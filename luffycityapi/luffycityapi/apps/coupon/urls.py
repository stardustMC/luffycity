from django.urls import path
from . import views


urlpatterns = [
    path("", views.CouponListAPIView.as_view(), name="coupon-list"),
    path("avail/", views.AvailableCouponListAPIView.as_view(), name="available-coupon-list"),
]