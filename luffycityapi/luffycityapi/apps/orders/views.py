from rest_framework import status
from rest_framework.response import Response

from .models import Order
from .serializers import OrderModelSerializer
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class OrderCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderModelSerializer

    def create(self, request, *args, **kwargs):
        res = super().create(request, *args, **kwargs)

        from django_redis import get_redis_connection
        redis = get_redis_connection("cart")
        user_id = request.user.id
        cart_count = redis.hlen(f"cart_{user_id}")
        return Response({"cart_count": cart_count, "order_number": res.data["order_number"]}, status=status.HTTP_201_CREATED)