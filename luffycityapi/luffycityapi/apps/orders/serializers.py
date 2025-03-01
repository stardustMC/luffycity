import logging
from django.db import transaction
from datetime import datetime
from rest_framework import serializers
from django_redis import get_redis_connection
from .models import Order, OrderDetail, Course


class OrderModelSerializer(serializers.ModelSerializer):
    pay_link = serializers.CharField(read_only=True)

    class Meta:
        model = Order
        fields = ["pay_type", "id", "order_number", "pay_link"]
        read_only_fields = ["id", "order_number"]
        extra_kwargs = {
            "pay_type": {"write_only": True},
        }

    def create(self, validated_data):
        """创建订单"""
        redis = get_redis_connection("cart")
        user_id = self.context["request"].user.id  # 1

        with transaction.atomic():
            t1 = transaction.savepoint()
            try:
                # 创建订单记录
                order = Order.objects.create(
                    name="购买课程",  # 订单标题
                    user_id=user_id,  # 当前下单的用户ID
                    order_number=datetime.now().strftime("%Y%m%d") + ("%08d" % user_id) + "%08d" % redis.incr("order_number"), # 基于redis生成分布式唯一订单号
                    pay_type=validated_data.get("pay_type"),  # 支付方式
                )

                # 记录本次下单的商品列表
                cart_hash = redis.hgetall(f"cart_{user_id}")
                if len(cart_hash) < 1:
                    raise serializers.ValidationError(detail="购物车没有要下单的商品")

                # 提取购物车中所有勾选状态为b'1'的商品
                course_id_list = [int(key.decode()) for key, value in cart_hash.items() if value == b'1']

                # 添加订单与课程的关系
                course_list = Course.objects.filter(pk__in=course_id_list, is_deleted=False, is_show=True).all()
                detail_list = []
                total_price = 0 # 本次订单的总价格
                real_price = 0  # 本次订单的实付总价

                for course in course_list:
                    discount_price = float(course.discount.get("price", 0)) # 获取课程原价
                    discount_name = course.discount.get("type", "")
                    detail_list.append(OrderDetail(
                        order=order,
                        course=course,
                        name=course.name,
                        price=course.price,
                        real_price=discount_price,
                        discount_name=discount_name,
                    ))

                    # 统计订单的总价和实付总价
                    total_price += float(course.price)
                    real_price += discount_price if discount_price > 0 else float(course.price)

                # 一次性批量添加本次下单的商品记录
                OrderDetail.objects.bulk_create(detail_list)
                # 保存订单的总价格和实付价格
                order.total_price = total_price
                order.real_price = real_price
                order.save()

                cart_hash = {key: value for key, value in cart_hash.items() if value == b'0'}
                pipe = redis.pipeline()
                pipe.multi()
                redis.hdel(f"cart_{user_id}")
                redis.hset(f"cart_{user_id}", mapping=cart_hash)
                pipe.execute()
            except Exception as e:
                logging.error("order create failed! %s" % e)
                transaction.savepoint_rollback(t1)
                raise serializers.ValidationError(detail="order create failed!")

        # todo 支付链接地址[后面实现支付功能的时候，再做]
        order.pay_link = ""
        return order