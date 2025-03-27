from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.filters import OrderingFilter
from rest_framework.views import APIView
from .pagination import CoursePageNumberPagination
from .models import CourseDirection, CourseCategory, Course, CourseChapter
from .serializers import CourseDirectionModelSerializer, CourseCategoryModelSerializer, CourseInfoModelSerializer, \
    CourseChapterModelSerializer


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
    filter_backends = [OrderingFilter, ]
    ordering_fields = ['id', 'students', 'orders']
    pagination_class = CoursePageNumberPagination

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

class CourseTypeChoiceAPIView(APIView):

    def get(self, request, *args, **kwargs):
        return Response(Course.course_type_choices, status=status.HTTP_200_OK)


from drf_haystack.viewsets import HaystackViewSet
from drf_haystack.filters import HaystackFilter
from .serializers import CourseIndexHaystackSerializer, CourseRetrieveModelSerializer
from .models import Course
from django_redis import get_redis_connection
import constants


class CourseSearchViewSet(HaystackViewSet):
    """课程信息全文搜索视图类"""
    # 指定本次搜索的最终真实数据的保存模型
    index_models = [Course]
    serializer_class = CourseIndexHaystackSerializer
    filter_backends = [OrderingFilter, HaystackFilter]
    ordering_fields = ('id', 'students', 'orders')
    pagination_class = CoursePageNumberPagination

    def list(self, request, *args, **kwargs):
        text = request.query_params.get("text")
        if text:
            redis = get_redis_connection("hot_words")
            key = f"{constants.DEFAULT_HOT_WORD}:{datetime.now().strftime('%Y:%m:%d')}"
            redis.zincrby(key, 1, text)  # 让有序集合中的text搜索关键字次数+1，如果该关键字第一次出现，则为1
            is_exists = redis.exists(key)
            if not is_exists:
                redis.expire(key, constants.HOT_WORD_EXPIRE * 24 * 3600)
        return super().list(request, *args, **kwargs)

class CourseRetrieveAPIView(RetrieveAPIView):
    """课程详情信息"""
    queryset = Course.objects.filter(is_show=True, is_deleted=False).all()
    serializer_class = CourseRetrieveModelSerializer

class CourseChapterListAPIView(ListAPIView):
    """课程章节列表"""
    serializer_class = CourseChapterModelSerializer
    def get_queryset(self):
        """列表页数据"""
        course = int(self.kwargs.get("course", 0))
        try:
            Course.objects.filter(pk=course).first()
        except:
            return []
        queryset = CourseChapter.objects.filter(course=course,is_show=True, is_deleted=False).order_by("orders", "id")
        return queryset.all()


from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime, timedelta

class HotWordAPIView(APIView):
    """搜索热词"""
    def get(self, request):
        redis = get_redis_connection("hot_words")
        # 获取最近指定天数的热词的key
        key_list = []
        for i in range(0, constants.HOT_WORD_EXPIRE):
            date = datetime.now() - timedelta(days=i)
            year = date.year
            month = date.month if date.month >= 10 else f"0{date.month}"
            day = date.day if date.day >= 10 else f"0{date.day}"
            key = f"{constants.DEFAULT_HOT_WORD}:{year}:{month}:{day}"
            key_list.append(key)

        # 先删除原有的统计最近几天的热搜词的有序统计集合
        redis.delete(constants.DEFAULT_HOT_WORD)
        # 根据date_list找到最近指定天数的所有集合，并完成并集计算，产生新的有序统计集合constants.DEFAULT_HOT_WORD
        redis.zunionstore(constants.DEFAULT_HOT_WORD, key_list, aggregate="sum")
        # 按分数store进行倒序显示排名靠前的指定数量的热词
        word_list = redis.zrevrange(constants.DEFAULT_HOT_WORD, 0, constants.HOT_WORD_LENGTH-1)
        return Response(word_list)
