from rest_framework import serializers
from .models import CourseDirection, CourseCategory, Course, Teacher, CourseChapter, CourseLesson


class CourseDirectionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseDirection
        fields = ['id', 'name']


class CourseCategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = ['id', 'name']

class CourseLessonModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseLesson
        fields = ['id', 'name', 'orders', 'get_lesson_type_display', 'duration']

class CourseInfoModelSerializer(serializers.ModelSerializer):
    lesson_list = CourseLessonModelSerializer(many=True)
    """课程信息的序列化器"""
    class Meta:
        model = Course
        fields = [
            "id", "name", "course_cover", "level", "get_level_display",
            "students", "status", "get_status_display",
            "lessons", "pub_lessons", "price", "discount", "credit", "lesson_list",
        ]


from django.conf import settings
from drf_haystack.serializers import HaystackSerializer
from .search_indexes import CourseIndex

class CourseIndexHaystackSerializer(HaystackSerializer):
    """课程搜索的序列化器"""
    class Meta:
        index_classes = [CourseIndex]
        fields = ["text", "id", "name", "course_cover", "get_level_display", "students", "get_status_display", "pub_lessons", "price", "discount", "orders"]

    def to_representation(self, instance):
        """用于指定返回数据的字段的"""
        # 课程的图片，在这里通过elasticsearch提供的，所以不会提供图片地址左边的域名的。因此在这里手动拼接
        instance.course_cover = f'//{settings.OSS_BUCKET_NAME}.{settings.OSS_ENDPOINT}/uploads/{instance.course_cover}'
        return super().to_representation(instance)

class CourseTeacherModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ["id", "name", "avatar", "role", "get_role_display", "title", "signature", "brief"]

class CourseChapterModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseChapter
        fields = ["id", "orders", "name", "summary", "get_lesson_list"]

class CourseRetrieveModelSerializer(serializers.ModelSerializer):
    """课程详情的序列化器"""
    direction_name = serializers.CharField(source="direction.name")
    # diretion = serializers.SlugRelatedField(read_only=True, slug_field='name')
    category_name = serializers.CharField(source="category.name")
    # 序列化器嵌套
    teacher = CourseTeacherModelSerializer()

    class Meta:
        model = Course
        fields = [
            "name", "course_cover", "course_video", "level", "get_level_display", "credit",
            "description", "pub_date", "status", "get_status_display", "students","discount",
            "lessons", "pub_lessons", "price", "direction", "direction_name", "category", "category_name", "teacher"
        ]