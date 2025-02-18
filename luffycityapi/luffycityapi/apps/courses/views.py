from rest_framework.generics import ListAPIView
from .models import CourseDirection, CourseCategory, Course
from .serializers import CourseDirectionModelSerializer, CourseCategoryModelSerializer, CourseInfoModelSerializer


# Create your views here.
class CourseDirectionListAPIView(ListAPIView):
    """学习方向"""
    queryset = CourseDirection.objects.filter(is_show=True, is_deleted=False).order_by("orders","id")
    serializer_class = CourseDirectionModelSerializer


class CourseCategoryListAPIView(ListAPIView):
    """courses direction"""
    serializer_class = CourseCategoryModelSerializer

    def get_queryset(self):
        queryset = CourseCategory.objects.filter(is_show=True, is_deleted=False)

        direction = int(self.kwargs.get("direction"))
        if direction and direction > 0:
            queryset = queryset.filter(direction_id=direction)

        return queryset.order_by("orders", "id").all()

class CourseListAPIView(ListAPIView):
    """课程列表接口"""
    serializer_class = CourseInfoModelSerializer

    def get_queryset(self):
        queryset = Course.objects.filter(is_deleted=False, is_show=True).order_by("-orders", "-id")
        direction = int(self.kwargs.get("direction", 0))
        category = int(self.kwargs.get("category", 0))
        # 只有在学习方向大于0的情况下才进行学习方向的过滤
        if direction > 0:
            queryset = queryset.filter(direction=direction)

        # 只有在课程分类大于0的情况下才进行课程分类的过滤
        if category > 0:
            queryset = queryset.filter(category=category)

        return queryset.all()