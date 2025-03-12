from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'^alipay/(?P<order_number>[0-9]+)/$', views.AliPayViewSet.as_view({'get': 'link'})),
    path('alipay/result/', views.AliPayViewSet.as_view({'get': 'pay_feedback'})),
    re_path('alipay/query/(?P<order_number>[0-9]+)/$', views.AliPayViewSet.as_view({'get': 'query'})),
]