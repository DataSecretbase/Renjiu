from django.core.validators import validate_email

from rest_framework import serializers, validators

from .models import *

class UserShareCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserShare
        fields = ("__all__")


class ShareGoodsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShareGoods
        fields = ("__all__")


class RebateLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = RebateLog
        fields = ("__all__")
