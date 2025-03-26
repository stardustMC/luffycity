from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView

from courses.models import Course
from .models import UserCourse

from .pagination import UserCoursePageNumberPagination
from .serializers import UserCourseSerializer


# Create your views here.
class CourseTypeAPIView(APIView):

    def get(self, request):
        return Response(Course.course_type, status=status.HTTP_200_OK)


class UserCourseListAPIView(ListAPIView):
    serializer_class = UserCourseSerializer
    pagination_class = UserCoursePageNumberPagination
    ordering_fields = ("id", )

    def get_queryset(self):
        user_id = self.request.user.id
        user_courses = UserCourse.objects.filter(user_id=user_id)

        course_type = self.request.query_params.get('course_type', -1)
        if course_type > -1:
            user_courses = user_courses.filter(course_course_type=course_type)
        return user_courses.all().order_by('id')