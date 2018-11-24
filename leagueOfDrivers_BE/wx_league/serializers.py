from django.utils.timezone import now
from rest_framework import serializers
from .models import *
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser


class CouponsSerializer(serializers.ModelSerializer):
    restOfDay = serializers.SerializerMethodField()

    class Meta:
        model = Coupons
        fields = ("id","money_min","money_hreshold","date_end_type","date_end_days","restOfDay","is_active","date_add", "goods_id")

    def get_restOfDay(self, obj):
        return (now() - obj.date_add).days

class IconSerializer(serializers.ModelSerializer):

    class Meta:
        model = Icon
        fields = ("__all__")


class WechatUserSerializer(serializers.ModelSerializer):
    avatar = IconSerializer(read_only=True)

    class Meta:
        model = WechatUser
        fields = ("name","gender","phone","get_address","avatar")

