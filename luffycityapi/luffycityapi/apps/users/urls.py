from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
import views

urlpatterns = [
    path('login/', obtain_jwt_token, name='login'),
]