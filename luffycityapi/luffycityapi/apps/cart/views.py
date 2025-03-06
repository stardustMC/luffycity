from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django_redis import get_redis_connection
from courses.models import Course

# Create your views here.
class CartAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user_id = request.user.id
        redis = get_redis_connection('cart')
        cart_hash = redis.hgetall('cart_%s' % user_id)
        if len(cart_hash) < 1:
            return Response({"error": "购物车没有任何商品。"})

        cart_dict = {int(k.decode("utf-8")): int(v.decode("utf-8")) for k, v in cart_hash.items()}

        course_id_list = [cid for cid, _ in cart_dict.items()]
        course_list = Course.objects.filter(pk__in=course_id_list, is_deleted=False, is_show=True).all()

        data = []
        for course in course_list:
            data.append({
                "id": course.id,
                "name": course.name,
                "course_cover": course.course_cover.url,
                "price": float(course.price),
                "discount": course.discount,
                "credit": course.credit,
                "course_type": course.get_course_type_display(),
                # 勾选状态：把课程ID转换成bytes类型，判断当前ID是否在购物车字典中作为key存在，如果存在，判断当前课程ID对应的值是否是字符串"1"，是则返回True
                "selected": course.id in cart_dict and cart_dict[course.id]
            })
        return Response({"errmsg": "courses in cart returned", "cart": data}, status=status.HTTP_200_OK)

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

    def patch(self, request):
        user_id = request.user.id
        course_id = int(request.data.get('course_id'))
        selected = int(bool(request.data.get('selected')))

        redis = get_redis_connection('cart')
        try:
            Course.objects.get(pk=course_id)
        except Course.DoesNotExist:
            redis.hdel('cart_%s' % user_id, course_id)
            return Response({"errmsg": "course not found, probably has been removed"}, status=status.HTTP_404_NOT_FOUND)

        redis.hset('cart_%s' % user_id, course_id, selected)
        return Response({"errmsg": "course select state patched."}, status=status.HTTP_200_OK)

    def put(self, request):
        user_id = request.user.id
        selected = int(bool(request.data.get('selected')))

        redis = get_redis_connection('cart')
        cart_hash = redis.hgetall('cart_%s' % user_id)
        cart_list = [int(k.decode("utf-8")) for k in cart_hash]

        pipe = redis.pipeline()
        pipe.multi()
        for course_id in cart_list:
            redis.hset('cart_%s' % user_id, course_id, selected)
        pipe.execute()

        return Response({"errmsg": "course all select state changed."}, status=status.HTTP_200_OK)

    def delete(self, request):
        user_id = request.user.id
        course_id = request.query_params.get('course_id')

        redis = get_redis_connection('cart')
        redis.hdel('cart_%s' % user_id, course_id)

        cart_count = redis.hlen('cart_%s' % user_id)
        return Response({"errmsg": "course removed from cart.", "cart_count": cart_count}, status=status.HTTP_200_OK)

class CartOrderAPIView(APIView):
    permission_classes = [IsAuthenticated,]

    def get(self, request):
        user_id = request.user.id
        redis = get_redis_connection('cart')
        cart_hash = redis.hgetall('cart_%s' % user_id)
        course_id_list = [int(k.decode("utf-8")) for k, v in cart_hash.items() if v == b'1']

        course_list = Course.objects.filter(pk__in=course_id_list, is_deleted=False, is_show=True).all()
        if len(course_list) < 1:
            return Response({"errmsg": "cart is empty! try shopping first~"}, status=status.HTTP_204_NO_CONTENT)

        data = []
        for course in course_list:
            data.append({
                "id": course.id,
                "name": course.name,
                "course_cover": course.course_cover.url,
                "price": float(course.price),
                "discount": course.discount,
                "credit": course.credit,
                "course_type": course.get_course_type_display(),
            })
        return Response({"errmsg": "courses in cart returned", "cart": data}, status=status.HTTP_200_OK)