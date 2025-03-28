from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

import constants
from .services import get_coupon_list, get_available_coupons


# Create your views here.
class CouponListAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        coupon_data = get_coupon_list(request.user.id)
        return Response(coupon_data, status=status.HTTP_200_OK)


class AvailableCouponListAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        available_coupons = get_available_coupons(request.user.id)
        return Response({
            "own_credit": request.user.credit,
            "msg": "OK",
            "available_coupons": available_coupons,
            "credit_ratio": constants.CREDIT_TO_DISCOUNT_PRICE
        }, status=status.HTTP_200_OK)
