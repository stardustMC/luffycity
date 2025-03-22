from faker import Faker
from random import randint
from datetime import datetime
from coupon.models import CouponLog, Coupon
from django.core.management import BaseCommand
from coupon.services import add_coupon_to_redis

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
        coupon_amount = Coupon.objects.count()
        for i in range(options["amount"]):
            user_id = randint(1, 3)
            instance = CouponLog.objects.create(
                name=faker.sentence(),
                user_id=user_id,
                coupon_id=randint(1, coupon_amount),
                use_time=datetime.now(),
                use_status = 0
            )
            add_coupon_to_redis(instance)