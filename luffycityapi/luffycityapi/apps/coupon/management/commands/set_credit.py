from django.core.management import BaseCommand
from courses.models import Course
from random import randint


class Command(BaseCommand):

    def handle(self, *args, **options):
        queryset = Course.objects.filter(is_deleted=False, is_show=True).all()
        for course in queryset:
            if course.id % 3 == 0:
                course.credit = randint(0, 10) * 10
                course.save()
