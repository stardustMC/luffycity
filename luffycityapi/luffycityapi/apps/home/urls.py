from . import views
from django.urls import path

urlpatterns = [
    path('nav/header/', views.NavHeaderListAPIView.as_view(), name='nav_header'),
    path('nav/footer/', views.NavFooterListAPIView.as_view(), name='nav_footer'),
]