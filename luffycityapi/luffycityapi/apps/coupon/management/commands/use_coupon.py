import json
from datetime import datetime
from django_redis import get_redis_connection
from faker import Faker
from random import randint
from coupon.models import CouponLog, Coupon
from orders.models import Order
from django.core.management import BaseCommand, CommandError


faker = Faker(['zh-CN', 'zh-TW'])
class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            "--amount",
            type=int,
            dest="amount",
            help="amount of coupon to put in use",
        )

    def handle(self, *args, **options):
        coupon_amount = Coupon.objects.all().count()
        order_amount = Order.objects.all().count()
        for i in range(options["amount"]):
            user_id = randint(1, 3)
            instance = CouponLog.objects.create(
                name=faker.sentence(),
                user_id=user_id,
                coupon_id=randint(1, coupon_amount),
                order_id=randint(1, order_amount),
                use_time=datetime.now(),
                use_status = 0
            )
            self.sync_redis(instance, user_id)

    def sync_redis(self, couponlog, user_id):
        # store coupon log in redis
        redis = get_redis_connection("coupon")
        hkey = "%s:%s" % (couponlog.coupon.id, user_id)
        pipe = redis.pipeline()
        pipe.multi()
        pipe.hset(hkey, "coupon_id", couponlog.coupon.id)
        pipe.hset(hkey, "name", couponlog.coupon.name)
        pipe.hset(hkey, "discount", couponlog.coupon.discount)
        pipe.hset(hkey, "get_discount_display", couponlog.coupon.get_discount_display())
        pipe.hset(hkey, "coupon_type", couponlog.coupon.coupon_type)
        pipe.hset(hkey, "get_coupon_type_display", couponlog.coupon.get_coupon_type_display())
        pipe.hset(hkey, "start_time", couponlog.coupon.start_time.strftime("%Y-%m-%d %H:%M:%S"))
        pipe.hset(hkey, "end_time", couponlog.coupon.end_time.strftime("%Y-%m-%d %H:%M:%S"))
        pipe.hset(hkey, "get_type", couponlog.coupon.get_type)
        pipe.hset(hkey, "get_get_type_display", couponlog.coupon.get_get_type_display())
        pipe.hset(hkey, "condition", couponlog.coupon.condition)
        pipe.hset(hkey, "sale", couponlog.coupon.sale)
        pipe.hset(hkey, "to_direction",
                  json.dumps(list(couponlog.coupon.to_direction.values("direction__id", "direction__name"))))
        pipe.hset(hkey, "to_category",
                  json.dumps(list(couponlog.coupon.to_category.values("category__id", "category__name"))))
        pipe.hset(hkey, "to_course",
                  json.dumps(list(couponlog.coupon.to_course.values("course__id", "course__name"))))
        pipe.expire(hkey, int(couponlog.coupon.end_time.timestamp() - datetime.now().timestamp()))
        pipe.execute()
