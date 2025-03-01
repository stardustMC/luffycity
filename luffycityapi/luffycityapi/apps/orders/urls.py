from . import views
from django.urls import path

urlpatterns = [
    path("", views.OrderCreateAPIView.as_view(), name="order_create"),
]