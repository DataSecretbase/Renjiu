from django.utils.timezone import now
from rest_framework import serializers
from rest_framework import validators
from .models import *
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from actstream.models import Action, followers, following
from actstream.actions import is_following

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


class AccountSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True, required=False)
    confirm_password = serializers.CharField(write_only=True, required=False)
    avatar = IconSerializer(required=False)

    class Meta:
        model = WechatUser
        fields = ('id', 'email', 'username', 'avatar', 'date_joined',
                  'updated_at', 'password', 'confirm_password')
        read_only_fields = ('date_joined', 'updated_at')


    def validate(self, attrs):
        if 'password' in attrs:
            if attrs['password'] != attrs['confirm_password']:
                raise serializers.ValidationError("Password is not matched with a confirm password")
        return attrs



    def update(self, instance, validated_data):
        # instance.email = validated_data.get('email', instance.email)
        # instance.username = validated_data.get('username', instance.username)
        instance.name = validated_data.get('name', instance.name)
        instance.openid = validated_data.get('openid', instance)
        instance.union_id = validated_data.get('union_id', )
        instance.avatar = validated_data.get('image', instance.avatar)

        instance.save()

        if self.checkPassword(validated_data):
            instance.set_password(validated_data.get('password'))
            instance.save()

        return instance


    def checkPassword(self, validated_data):
        password = validated_data.get('password', None)
        confirm_password = validated_data.get('confirm_password', None)

        if password and confirm_password and password == confirm_password:
            return True
        return False



class UserSerializer(serializers.ModelSerializer):
    avatar = IconSerializer(read_only=False)

    class Meta:
        model = WechatUser
        fields = ('id', 'username',  'email', 'avatar', 'name')
        read_only_fields = ('id', 'username', 'email')


    def to_representation(self, obj):
        return_obj = super(UserSerializer, self).to_representation(obj)
        followers_count = len(followers(obj))
        following_count = len(following(obj))

        new_obj = {
            "following": following_count,
            "followers": followers_count
        }
        return_obj.update(new_obj)
        return return_obj


class ViewedProfileTrackingSerializer(serializers.ModelSerializer):
    actor = UserSerializer(default=serializers.CurrentUserDefault(), read_only=True)
    visited_profile = UserSerializer(default=serializers.CurrentUserDefault(), read_only=True)
    class Meta:
        model = ViewedProfileTracking
        fields = ('actor', 'visited_profile', 'visited_time')


class GenericRelatedField(serializers.Field):
    def to_representation(self, value):
        if isinstance(value, User):
            return UserSerializer(value).data
        # Not found - return string.
        return str(value)


class ActionSerializer(serializers.ModelSerializer):
    actor = GenericRelatedField(read_only=True)
    target = GenericRelatedField(read_only=True)
    action_object = GenericRelatedField(read_only=True)

    class Meta:
        model = Action
        fields = '__all__'