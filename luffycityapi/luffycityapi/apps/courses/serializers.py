from rest_framework import serializers
from .models import CourseDirection, CourseCategory


class CourseDirectionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseDirection
        fields = ['id', 'name']


class CourseCategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = ['id', 'name']