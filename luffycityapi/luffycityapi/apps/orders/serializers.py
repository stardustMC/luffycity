import logging
from django.db import transaction
from datetime import datetime
from rest_framework import serializers
from django_redis import get_redis_connection

from coupon.models import CouponLog
from .models import Order, OrderDetail, Course


class OrderModelSerializer(serializers.ModelSerializer):
    pay_link = serializers.CharField(read_only=True)
    coupon_id = serializers.IntegerField(write_only=True, default=-1)

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

        # 找到优惠券的记录
        user_coupon_id = validated_data.get("id", -1)
        user_coupon = CouponLog.objects.filter(pk=user_coupon_id, user_id=user_id).first()

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

                max_discount_course = None
                for course in course_list:
                    discount_price = course.discount.get("price", None) # 获取课程优惠折扣
                    if discount_price is not None:
                        discount_price = float(discount_price)
                    discount_name = course.discount.get("type", "")
                    detail_list.append(OrderDetail(
                        order=order,
                        course=course,
                        name=course.name,
                        price=course.price,
                        real_price=discount_price or course.price,
                        discount_name=discount_name,
                    ))

                    # 找出能最大发挥优惠券力度的课程（也就是最贵的课程使用折扣优惠券）
                    if user_coupon and discount_price is None:
                        if max_discount_course is None or course.price > max_discount_course.price:
                            max_discount_course = course

                    # 统计订单的总价和实付总价
                    total_price += float(course.price)
                    real_price += discount_price or float(course.price)

                coupon_discount_price = 0
                if user_coupon:
                    sale = float(user_coupon.coupon.sale[1:])
                    # 减免
                    if user_coupon.coupon.discount == 1:
                        coupon_discount_price = sale
                    # 折扣
                    elif user_coupon.coupon.discount == 2:
                        coupon_discount_price = float(max_discount_course.price) * (1 - sale)

                # 一次性批量添加本次下单的商品记录
                OrderDetail.objects.bulk_create(detail_list)
                # 保存订单的总价格和实付价格
                order.total_price = total_price
                order.real_price = float(real_price - coupon_discount_price)
                order.save()

                cart = {key: value for key, value in cart_hash.items() if value == b'0'}
                pipe = redis.pipeline()
                pipe.multi()
                pipe.delete(f"cart_{user_id}")
                if cart:
                    pipe.hset(f"cart_{user_id}", mapping=cart)
                pipe.execute()
                # update couponlog status
                user_coupon.order = order
                user_coupon.use_time = datetime.now()
                user_coupon.use_status = 1
                user_coupon.save()
                # sync coupon data in redis
                coupon_redis = get_redis_connection("coupon")
                coupon_redis.delete(f"{user_coupon.id}:{user_id}")
            except Exception as e:
                logging.error("order create failed! %s" % e)
                transaction.savepoint_rollback(t1)
                raise serializers.ValidationError(detail="order create failed!")

        # todo 支付链接地址[后面实现支付功能的时候，再做]
        order.pay_link = ""
        return order