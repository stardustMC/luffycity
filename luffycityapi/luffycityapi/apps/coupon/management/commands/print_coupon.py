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
        queryset = Course.objects.all().order_by("id")
        self.course_range = queryset.first().id, queryset.last().id
        queryset = CourseDirection.objects.all().order_by("id")
        self.direction_range = queryset.first().id, queryset.last().id
        queryset = CourseCategory.objects.all().order_by("id")
        self.category_range = queryset.first().id, queryset.last().id
        self.total = Coupon.objects.all().order_by("id").first().id

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
            total = (20, 50, 100)[randint(0, 2)]
            coupon_type = randint(0, 3)
            Coupon.objects.create(
                name=faker.canton_name() + " Coupon",
                discount=discount,
                sale=('-' if discount == 1 else '*') + str(value),
                coupon_type = coupon_type,
                total = total,
                has_total = total,
                start_time = datetime.now(),
                end_time = datetime.now() + timedelta(days=30 * 6),
                get_type = randint(0, 1),
                condition = value * 2 if discount == 1 else 500,
                per_limit = randint(1, 5)
            )
            # course direction specified
            if coupon_type == 1:
                l, r = self.direction_range[0], self.direction_range[1]
                for i in range((r - l) // 5 + 1):
                    CouponDirection.objects.create(
                        direction_id=randint(l, r),
                        # we just printed it
                        coupon_id=self.total + 1,
                        created_time=datetime.now(),
                    )
            # course category specified
            elif coupon_type == 2:
                l, r = self.course_range[0], self.course_range[1]
                for i in range((r - l) // 6 + 1):
                    CouponCourseCat.objects.create(
                        category_id=randint(l, r),
                        # we just printed it
                        coupon_id=self.total + 1,
                        created_time=datetime.now(),
                    )
            # course specified
            elif coupon_type == 3:
                l, r = self.course_range[0], self.course_range[1]
                for i in range((r - l) // 10 + 1):
                    CouponCourse.objects.create(
                        course_id=randint(l, r),
                        # we just printed it
                        coupon_id=self.total + 1,
                        created_time=datetime.now(),
                    )
            self.total += 1