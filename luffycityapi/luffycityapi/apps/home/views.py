import constants
from .serializers import NavListSerializer, BannerListSerializer
from .models import Nav, Banner
from views import CachePageListAPIView
from rest_framework.generics import ListAPIView

import logging
logger = logging.getLogger("django")

# Create your views here.
class NavHeaderListAPIView(CachePageListAPIView):
    queryset = Nav.objects.filter(position=constants.NAV_HEADER_POSITION, is_show=True, is_deleted=False) \
        .order_by('orders', '-id')[:constants.NAV_HEADER_SIZE]
    serializer_class = NavListSerializer

class NavFooterListAPIView(CachePageListAPIView):
    queryset = Nav.objects.filter(position=constants.NAV_FOOTER_POSITION, is_show=True, is_deleted=False) \
        .order_by('orders', '-id')[:constants.NAV_FOOTER_SIZE]
    serializer_class = NavListSerializer

class BannerListAPIView(CachePageListAPIView):
    queryset = Banner.objects.filter(is_show=True, is_deleted=False) \
        .order_by('orders', '-id')[:constants.BANNER_SIZE]
    serializer_class = BannerListSerializer