from rest_framework.generics import ListAPIView
from .models import CourseDirection, CourseCategory
from .serializers import CourseDirectionModelSerializer, CourseCategoryModelSerializer


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