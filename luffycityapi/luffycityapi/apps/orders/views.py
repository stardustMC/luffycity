import constants
from .models import Order
from coupon.services import add_coupon_to_redis
from .pagination import OrderPageNumberPagination
from .serializers import OrderModelSerializer, OrderListModelSerializer

from django.http import Http404
from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView, ListAPIView


# Create your views here.
class OrderCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderModelSerializer

    def create(self, request, *args, **kwargs):
        res = super().create(request, *args, **kwargs)

        from django_redis import get_redis_connection
        redis = get_redis_connection("cart")
        user_id = request.user.id
        cart_count = redis.hlen(f"cart_{user_id}")
        return Response({
            "cart_count": cart_count,
            "order_number": res.data["order_number"],
            "timeout":     constants.ORDER_EXPIRE_TIME
        }, status=status.HTTP_201_CREATED)

class OrderStatusChoiceAPIView(APIView):

    def get(self, request, *args, **kwargs):
        return Response(Order.status_choices)

class OrderListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    ordering_fields = ["id"]
    serializer_class = OrderListModelSerializer
    pagination_class = OrderPageNumberPagination

    def get_queryset(self):
        queryset = Order.objects.filter(is_deleted=False, is_show=True, user_id=self.request.user.id)
        status_list = [item[0] for item in Order.status_choices]
        status = int(self.request.query_params.get("status", -1))
        if status in status_list:
            queryset = queryset.filter(order_status=status)
        return queryset.all()

class OrderViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def pay_cancel(self, request, *args, **kwargs):
        try:
            order = get_object_or_404(Order, *args, **kwargs)
        except Http404:
            return Response({"errmsg": "订单不存在！"}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            s1 = transaction.savepoint()
            try:
                coupon_log = order.to_coupon.first()
                if coupon_log:
                    add_coupon_to_redis(coupon_log)

                if order.credit > 0:
                    order.user.credit += order.credit
                    order.user.save()

                order.order_status = 2
                order.save()
                return Response({"errmsg": "当前订单已取消"}, status=status.HTTP_200_OK)
            except Exception:
                transaction.savepoint_rollback(s1)
                return Response({"errmsg": "订单取消发生错误！"}, status=status.HTTP_400_BAD_REQUEST)