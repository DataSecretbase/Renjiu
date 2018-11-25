from django.core.validators import validate_email

from rest_framework import serializers, validators
from wx_league import serializers as lea_serializer
from wx_league import models as wx_league
from .models import *


class UserShareCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShareUser
        fields = ("__all__",)


class UserShareSerializer(serializers.ModelSerializer):
    user = lea_serializer.WechatUserSerializer(read_only=True)

    class Meta:
        model = ShareUser
        fields = ("user", "first_leader", "second_leader", "third_leader")


class ShareGoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShareGoods
        fields = ("__all__",)


class RebateLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = RebateLog
        fields = ("__all__",)


class ShareUserProfileSerializer(serializers.ModelSerializer):
    user = UserShareSerializer(read_only=True)

    class Meta:
        model = ShareUserProfile
        fields = ("user", "total_price", "price", "cash_price",
                  "total_cash", "un_pay", "team_count", "order_money", "share_qrcode")


class CashCreateSerializer(serializers.ModelSerializer):
    user = UserShareSerializer(read_only=True)
    class Meta:
        model = Cash
        fields = ('user', 'cash')

    @staticmethod
    def check_balance(price, validated_data):
        cash = validated_data.get('cash', None)
        price = price

        if cash <= price:
            return True
        return

    def get_shareuser(self,cookie):
        return ShareUser.objects.get(user=wx_league.WechatUser.objects.get(cookie = cookie))


class CashListSerializer(serializers.ModelSerializer):
    user = UserShareSerializer(read_only=True)

    class Meta:
        model = Cash
        fields = ('user', 'cash', 'add_time', 'status')



    def create(self, instance,validated_data):
        instance.user = self.get_shareuser(validated_data.get("cookie", None))
        user = auth.check_cookie(self, user_type="ShareUserProfile" )
        instance.cash=0
        if self.check_balance(user["userobj"].price, validated_data.get("cash",0)):
            instance.cash = validated_data.get("cash", 0)
        instance.save()
        return instance
