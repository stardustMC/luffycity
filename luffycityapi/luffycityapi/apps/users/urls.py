from django.urls import path, re_path
from rest_framework_jwt.views import obtain_jwt_token
from .views import UserCourseListAPIView

urlpatterns = [
    path('login/', obtain_jwt_token, name='login'),
    path('course/', UserCourseListAPIView.as_view(), name='courses'),
]