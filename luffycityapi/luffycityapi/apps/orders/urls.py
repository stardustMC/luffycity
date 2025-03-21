from . import views
from django.urls import path

urlpatterns = [
    path("", views.OrderCreateAPIView.as_view(), name="order_create"),
    path("list/", views.OrderListAPIView.as_view(), name="order_list"),
    path("status/", views.OrderStatusChoiceAPIView.as_view(), name="order_status"),
]