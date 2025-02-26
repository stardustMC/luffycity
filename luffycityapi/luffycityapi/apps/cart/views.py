from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django_redis import get_redis_connection
from courses.models import Course

# Create your views here.
class CartAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        user_id = request.user.id
        course_id = request.data.get('course_id')
        selected = 1

        try:
            Course.objects.get(pk=course_id)
        except Course.DoesNotExist:
            return Response({"errmsg": "course not found"}, status=status.HTTP_404_NOT_FOUND)

        redis = get_redis_connection('cart')
        redis.hset('cart_%s' % user_id, course_id, selected)
        cart_count = redis.hlen('cart_%s' % user_id)
        return Response({"errmsg": "course added to cart~", "cart_count": cart_count}, status=status.HTTP_201_CREATED)
