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
    first_leader = lea_serializer.WechatUserSerializer(read_only=True)
    second_leader = lea_serializer.WechatUserSerializer(read_only=True)
    third_leader = lea_serializer.WechatUserSerializer(read_only=True)


    class Meta:
        model = ShareUser
        fields = ("user", "first_leader", "second_leader", "third_leader", "add_time")

    def to_representation(self, obj):
        print("obj")

        print(obj)
        returnObj = super(UserShareSerializer,self).to_representation(obj)
        total_price = ShareUserProfile.objects.get(user=obj).total_price
        order_num = len(wx_league.Order.objects.filter(wechat_user_id=obj.user, status=4))
        people_num = len(ShareUser.objects.filter(user=obj.user))
        new_obj = {}
        new_obj.update({
            "total_price": total_price,
            "order_num": order_num,
            'people_num': people_num
        })
        returnObj.update(new_obj)
        return returnObj

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
        fields = ('user', 'cash', 'add_time', 'get_status_display')

    def create(self, instance,validated_data):
        instance.user = self.get_shareuser(validated_data.get("cookie", None))
        user = auth.check_cookie(self, user_type="ShareUserProfile" )
        instance.cash=0
        if self.check_balance(user["userobj"].price, validated_data.get("cash",0)):
            instance.cash = validated_data.get("cash", 0)
        instance.save()
        return instance


class ShareOrderGoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShareOrderGoods
        fields = ("__all__",)



class ShareOrderSerializer(serializers.ModelSerializer):
    wechat_user_id = lea_serializer.WechatUserSerializer(read_only=True)

    class Meta:
        model = wx_league.Order
        fields = '__all__'

    def to_representation(self, obj):
        returnObj = super(ShareOrderSerializer,self).to_representation(obj)
        goods = ShareOrderGoods.objects.filter(order=obj)
        serializer = ShareGoodsSerializer(goods,many=True)
        new_obj = {}
        new_obj.update({
            "ShareGoods": serializer.data,
        })
        returnObj.update(new_obj)
        return returnObj


class ShareOrderTeamSerializer(serializers.ModelSerializer):
    wechat_user_id = lea_serializer.WechatUserSerializer(read_only=True)

    class Meta:
        model = wx_league.Order
        fields = '__all__'

    def to_representation(self, obj):
        returnObj = super(ShareOrderTeamSerializer, self).to_representation(obj)
        goods = ShareOrderGoods.objects.filter(order=obj)
        total = 0
        for good in goods:
            total += good.total*eval(good.sharegoods.get_cash_scheme_display())[2]
            print(eval(good.sharegoods.get_cash_scheme_display())[2])
        serializer = ShareGoodsSerializer(goods, many=True)
        new_obj = {}
        new_obj.update({
            "ShareGoods": serializer.data,
        })
        returnObj.update(new_obj)
        return returnObj
