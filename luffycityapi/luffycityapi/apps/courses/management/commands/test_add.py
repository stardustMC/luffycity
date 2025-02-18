#! /home/caoruchen/anaconda3/envs/luffycity/bin/python

import random
import os, sys
from faker import Faker
from django.conf import settings
from courses.models import Teacher, CourseDirection, CourseCategory
from django.core.management.base import BaseCommand, CommandError

faker = Faker(['zh_CN'])

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '--type',
            dest='type',
            default="teacher",
            type=str,
            help="Type of data",
        )
        parser.add_argument(
            '--number',
            dest='number',
            default=10,
            type=int,
            help='amount of data',
        )

    def handle(self, *args, **options):
        if options['type'] == 'teacher':
            self.add_teacher(options)
        elif options['type'] == 'direction':
            self.add_direction(options)
        elif options['type'] == 'category':
            self.add_category(options)
        else:
            raise CommandError("Type must be in ['teacher' 'direction' 'category']")

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
        print(f"{options['number']} items of {options['type']} data added in total.")

    def add_direction(self, options):
        for i in range(options['number']):
            CourseDirection.objects.create(
                name=faker.job(),
                remark=faker.sentence(),
                recomment_home_hot=False,
                recomment_home_top=False,
            )
        print(f"{options['number']} items of {options['type']} data added in total.")

    def add_category(self, options):
        for i in range(options['number']):
            CourseCategory.objects.create(
                name=faker.company(),
                remark=faker.sentence(),
                direction_id=random.randint(1, 10),
            )
        print(f"{options['number']} items of {options['type']} data added in total.")