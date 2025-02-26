from . import views
from django.urls import path

urlpatterns = [
    path("", views.CartAPIView.as_view(), name="cart"),
]