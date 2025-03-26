from rest_framework import serializers
from users.models import UserCourse
from courses.serializers import CourseInfoModelSerializer


class UserCourseSerializer(serializers.ModelSerializer):
    info = CourseInfoModelSerializer(source='course')

    class Meta:
        model = UserCourse
        fields = ["id", "info", "study_time"]