import constants
from .serializers import NavListSerializer, BannerListSerializer
from .models import Nav, Banner
from rest_framework.generics import ListAPIView

import logging
logger = logging.getLogger("django")

# Create your views here.
class NavHeaderListAPIView(ListAPIView):
    queryset = Nav.objects.filter(position=constants.NAV_HEADER_POSITION, is_show=True, is_deleted=False) \
        .order_by('orders', '-id')[:constants.NAV_HEADER_SIZE]
    serializer_class = NavListSerializer

class NavFooterListAPIView(ListAPIView):
    queryset = Nav.objects.filter(position=constants.NAV_FOOTER_POSITION, is_show=True, is_deleted=False) \
        .order_by('orders', '-id')[:constants.NAV_FOOTER_SIZE]
    serializer_class = NavListSerializer

class BannerListAPIView(ListAPIView):
    queryset = Banner.objects.filter(is_show=True, is_deleted=False) \
        .order_by('orders', '-id')[:constants.BANNER_SIZE]
    serializer_class = BannerListSerializer