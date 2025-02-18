from django.urls import path,re_path
from . import views


urlpatterns = [
    path("directions/", views.CourseDirectionListAPIView.as_view(), name="direction"),
    # path("category/", views.CourseCategoryListAPIView.as_view(), name="category"),
    re_path("category/(?P<direction>\d+)/", views.CourseCategoryListAPIView.as_view(), name="category"),
    re_path(r"^(?P<direction>\d+)/(?P<category>\d+)/$", views.CourseListAPIView.as_view()),
]