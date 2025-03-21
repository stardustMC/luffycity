from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

import constants
from .models import Order
from .pagination import OrderPageNumberPagination
from .serializers import OrderModelSerializer, OrderListModelSerializer
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class OrderCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    # queryset = Order.objects.all()
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