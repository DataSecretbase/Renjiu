from django.core.validators import validate_email

from rest_framework import serializers, validators

from .models import *
from base import serializers as base_serializers

class CategorySerializer(serializers.ModelSerializer):
    icon = base_serializers.IconSerializer(read_only = True)
    class Meta:
        model = Category
        fields = ('id', 'name', 'eng_name', 'category_type', 'pid', 'icon', 'level','sort')


class GoodsSerializer(serializers.ModelSerializer):

    category_id = CategorySerializer(read_only = True)
    pic = base_serializers.IconSerializer(read_only = True)

    class Meta:
        model = Goods
        fields = ('id','category_id','name','characteristic','date_add',
                'min_score','number_good_reputation','number_orders',
                'original_price','pic','pingtuan','shop_id','status','stores','video_id','views','weight')
        read_only_fields = ('date_add',)

    def update(self, instance, validated_data):
        instance.category_id = validated_data.get('category_id', instance.category_id)
        instance.characteristic = validated_data.get('characteristic', instance.characteristic)
        instance.logistics_id = validated_data.get('logistics_id', instance.logistics_id)
        instance.min_score = validated_data.get('min_score', instance.min_score)
        instance.store = validated_data.get('store', instance.store)
        instance.number_good_reputation = validated_data.get('number_good_reputation', instance.number_good_reputation)
        instance.save()


class GoodsReputationSerializer(serializers.ModelSerializer):

    class Meta:
        model = GoodsReputation
        fields = ("_all__")




class PreferentialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Preferential
        fields = ("id", "goods_info", "goods", "off", "date_create", "date_end", "preferential_type")


class GoodsPurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("__all__")


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("__all__")


