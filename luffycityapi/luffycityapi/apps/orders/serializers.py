import logging
from django.db import transaction
from datetime import datetime
from rest_framework import serializers
from django_redis import get_redis_connection

import constants
from coupon.models import CouponLog
from .models import Order, OrderDetail, Course


class OrderModelSerializer(serializers.ModelSerializer):
    # pay_link = serializers.CharField(read_only=True)
    coupon_id = serializers.IntegerField(write_only=True, default=-1)
    discount_type = serializers.IntegerField(write_only=True, default=0)

    class Meta:
        model = Order
        # fields = ["pay_type", "id", "order_number", "pay_link", "coupon_id", "discount_type"]
        fields = ["pay_type", "id", "order_number", "coupon_id", "discount_type"]
        read_only_fields = ["id", "order_number"]
        extra_kwargs = {
            "pay_type": {"write_only": True},
        }

    def create(self, validated_data):
        """创建订单"""
        redis = get_redis_connection("cart")
        user = self.context["request"].user
        user_id = user.id  # 1

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
                max_deduct_credits = 0
                for course in course_list:
                    if course.credit > 0:
                        max_deduct_credits += course.credit

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

                # 一次性批量添加本次下单的商品记录
                OrderDetail.objects.bulk_create(detail_list)

                discount_type = validated_data.get("discount_type", 0)
                # 使用优惠券
                if discount_type == 0 and user_coupon:
                    coupon_discount_price = 0
                    sale = float(user_coupon.coupon.sale[1:])
                    # 减免
                    if user_coupon.coupon.discount == 1:
                        coupon_discount_price = sale
                    # 折扣
                    elif user_coupon.coupon.discount == 2:
                        coupon_discount_price = float(max_discount_course.price) * (1 - sale)

                    order.real_price = float(real_price - coupon_discount_price)

                    # update couponlog status
                    user_coupon.order = order
                    user_coupon.use_time = datetime.now()
                    user_coupon.use_status = 1
                    user_coupon.save()
                    # sync coupon data in redis
                    coupon_redis = get_redis_connection("coupon")
                    coupon_redis.delete(f"{user_coupon.id}:{user_id}")
                # 使用积分
                elif discount_type == 1:
                    credit = validated_data.get("credit", 0)
                    # 用户积分不足
                    if credit > user.credit:
                        raise serializers.ValidationError("Oops! You don't have enough credits...")
                    # 超过了课程规定可用积分
                    if credit > max_deduct_credits:
                        raise serializers.ValidationError("Oops! credit limit exceeded %d ..." % max_deduct_credits)
                    # 超过了订单实付金额（例如免费课程）
                    if credit > real_price * constants.CREDIT_TO_DISCOUNT_PRICE:
                        raise serializers.ValidationError(f"Oops! You can only use {real_price * constants.CREDIT_TO_DISCOUNT_PRICE} credits at most!")

                    order.real_price = float(real_price - float(credit / constants.CREDIT_TO_DISCOUNT_PRICE))
                    # 用户扣除积分
                    user.credit -= credit
                    user.save()
                else:
                    order.real_price = real_price

                cart = {key: value for key, value in cart_hash.items() if value == b'0'}
                pipe = redis.pipeline()
                pipe.multi()
                pipe.delete(f"cart_{user_id}")
                if cart:
                    pipe.hset(f"cart_{user_id}", mapping=cart)
                pipe.execute()
                # 保存订单的总价格
                order.total_price = total_price
                order.save()
            except Exception as e:
                logging.error("order create failed! %s" % e)
                transaction.savepoint_rollback(t1)
                raise serializers.ValidationError(detail="order create failed!")
        return order