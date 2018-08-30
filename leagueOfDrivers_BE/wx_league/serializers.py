from django.utils.timezone import now
from rest_framework import serializers
from .models import *
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser


class CouponsSerializer(serializers.ModelSerializer):
    restOfDay = serializers.SerializerMethodField()

    class Meta:
        model = Coupons
        fields = ("id","moneyMin","moneyHreshold","dateEndType","dateEndDays","restOfDay","is_active","date_add", "goods_id")

    def get_restOfDay(self, obj):
        return (now() - obj.date_add).days

