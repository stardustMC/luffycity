#! /home/caoruchen/anaconda3/envs/luffycity/bin/python

import random
from datetime import datetime
from faker import Faker
from courses.models import Teacher, CourseDirection, CourseCategory, Course, CourseChapter, CourseLesson, CourseActivityPrice
from django.core.management.base import BaseCommand, CommandError

faker = Faker(['zh_CN'])

class Command(BaseCommand):

    def __init__(self):
        super(Command, self).__init__()
        self.fields = ["teacher", "direction", "category", "course", "actprice"]
        self.default_amount = 10
        self.default_chapter = 5
        self.default_lesson = 3

    def add_arguments(self, parser):
        parser.add_argument(
            '--type',
            dest='type',
            default=self.fields[0],
            type=str,
            help="Type of data",
        )
        parser.add_argument(
            '--number',
            dest='number',
            default=self.default_amount,
            type=int,
            help='amount of data',
        )

    def handle(self, *args, **options):
        data_type = options['type']
        if data_type in self.fields:
            if hasattr(self, "add_%s" % data_type):
                try:
                    getattr(self, "add_%s" % data_type)(options)
                except Exception as e:
                    print("command failed due to %s" % e, "Maybe should use 'truncate' to clear table")
            else:
                raise CommandError(f"Type {data_type} is in fields but not implemented.")
        else:
            print(f"Type {data_type} is not supported. Try ", self.fields)

    def add_teacher(self, options):
        for i in range(options['number']):
            Teacher.objects.create(
                name=faker.name(),
                title="teacher",
                signature="Alex dashabi",
                role=random.randint(0, 2),
                avatar="teacher/avatar.jpg",
                brief=f"从业3年，管理班级无数，联系电话：{faker.unique.phone_number()}，邮箱地址：{faker.unique.company_email()}",
            )

    def add_direction(self, options):
        for i in range(options['number']):
            CourseDirection.objects.create(
                name=faker.job(),
                remark=faker.sentence(),
                recomment_home_hot=False,
                recomment_home_top=False,
            )

    def add_category(self, options):
        for i in range(options['number']):
            CourseCategory.objects.create(
                name=faker.job_male()[:3] + faker.job_female()[:3],
                remark=faker.sentence(),
                direction_id=random.randint(1, CourseDirection.objects.count()),
            )

    def add_course(self, options):
        for i in range(options['number']):
            name = faker.job() + "课程"
            Course.objects.create(
                name=name,
                orders = 1,
                is_show=1,
                is_deleted=0,
                created_time=datetime.now(),
                updated_time=datetime.now(),
                course_cover=f"course/cover/course-{random.randint(1, 20)}.png",
                course_video="",
                course_type=random.randint(0, 2),
                level=random.randint(0, 2),
                description="<p>"+name+"</p>",
                pub_date=f"2024-{random.randint(1, 12)}-{random.randint(1, 28)}",
                period=random.randint(7, 90),
                attachment_path="luffycity-celery用法1.zip",
                attachment_link=None,
                status=random.randint(0, 2),
                students=random.randint(1000, 2000),
                lessons=random.randint(50, 200),
                pub_lessons=random.randint(30, 50),
                price=faker.random_number(4, True),
                recomment_home_hot=0,
                recomment_home_top=0,
                category_id=random.randint(1, CourseCategory.objects.count()),
                direction_id=random.randint(1, CourseDirection.objects.count()),
                teacher_id=random.randint(1, 6),
            )

        queryset = Course.objects.all().filter(is_deleted=False).order_by("id")
        min_id, max_id = queryset.first().id, queryset.last().id
        for idx in range(min_id, max_id + 1):
            for chapter in range(self.default_chapter):
                instance = CourseChapter.objects.create(
                    name=f"第{chapter + 1}章节",
                    is_show=1,
                    is_deleted=0,
                    created_time=datetime.now(),
                    updated_time=datetime.now(),
                    orders=chapter + 1,
                    summary=faker.sentence(),
                    pub_date=datetime.now(),
                    course_id=idx,
                )
                for lesson in range(self.default_lesson):
                    CourseLesson.objects.create(
                        name=f"第{lesson + 1}课时",
                        is_show=1,
                        is_deleted=0,
                        created_time=datetime.now(),
                        updated_time=datetime.now(),
                        orders=lesson + 1,
                        lesson_type=2,
                        lesson_link="1.mp4",
                        duration=f"{random.randint(1, 60)}:{random.randint(1, 60)}",
                        pub_date=datetime.now(),
                        free_trail=random.randint(0, 1),
                        recomment=random.randint(0, 1),
                        chapter_id=instance.id,
                        course_id=idx,
                    )

    def add_actprice(self, options):
        course_total = Course.objects.filter().count()
        for idx in range(1, course_total + 1):
            # 三分之一的课程不参与优惠活动
            if idx % 3:
                continue
            discount_id = random.randint(1, 3)
            CourseActivityPrice.objects.create(
                name=["九折大优惠", "免费送课", "满减促销"][discount_id - 1],
                course_id=idx,
                discount_id=discount_id,
                activity_id=1
            )
