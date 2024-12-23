from rest_framework import serializers
from .models import Nav, Banner


class NavListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nav
        fields = ['name', 'link', 'is_http']

class BannerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['name', 'link', 'image', 'is_http']
