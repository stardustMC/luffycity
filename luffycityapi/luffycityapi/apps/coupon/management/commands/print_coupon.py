from faker import Faker
from random import randint
from datetime import datetime, timedelta
from django.core.management import BaseCommand
from courses.models import Course, CourseDirection, CourseCategory
from coupon.models import Coupon, CouponDirection, CouponCourseCat, CouponCourse


faker = Faker(["zh-CN"])

class Command(BaseCommand):

    def __init__(self):
        super(Command, self).__init__()
        self.course_count = Course.objects.count()
        self.direction_count = CourseDirection.objects.count()
        self.category_count = CourseCategory.objects.count()

    def add_arguments(self, parser):
        parser.add_argument(
            '--amount',
            type=int,
            dest='amount',
            default=100,
            help="Amount of coupons to print",
        )

    def handle(self, *args, **options):
        for i in range(options["amount"]):
            discount = randint(1, 2)
            if discount == 1:
                value = randint(200, 1000)
            else:
                value = randint(50, 99) / 100

            coupon_type = randint(0, 3)
            coupon = Coupon.objects.create(
                name=faker.job() + " 优惠券",
                discount=discount,
                sale=('-' if discount == 1 else '*') + str(value),
                coupon_type = coupon_type,
                total = 50,
                has_total = 50,
                start_time = datetime.now(),
                end_time = datetime.now() + timedelta(days=30 * 6),
                get_type = randint(0, 1),
                condition = value * 2 if discount == 1 else 500,
                per_limit = randint(1, 5)
            )
            # course direction specified
            if coupon_type == 1:
                for i in range(self.direction_count // 5 + 1):
                    CouponDirection.objects.create(
                        direction_id=randint(1, self.direction_count),
                        # we just printed it
                        coupon_id=coupon.id,
                        created_time=datetime.now(),
                    )
            # course category specified
            elif coupon_type == 2:
                for i in range(self.category_count // 8 + 1):
                    CouponCourseCat.objects.create(
                        category_id=randint(1, self.category_count),
                        # we just printed it
                        coupon_id=coupon.id,
                        created_time=datetime.now(),
                    )
            # course specified
            elif coupon_type == 3:
                for i in range(self.course_count // 10 + 1):
                    CouponCourse.objects.create(
                        course_id=randint(1, self.course_count),
                        # we just printed it
                        coupon_id=coupon.id,
                        created_time=datetime.now(),
                    )