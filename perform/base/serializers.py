from django.core.validators import validate_email

from life.models import Topic
from actstream.models import Action, followers, following
from actstream.actions import is_following


from rest_framework import serializers, validators
from .models import *


class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True, required = False)
    confirm_password = serializers.CharField(write_only = True, required = True)

    class Meta:
        model = User
        fields = ('id','email','username','first_name','last_name','full_name','password','confirm_password',)
        read_only_fields = ('full_name',)
        
        def validate(self, attrs):
            if 'password' in attrs:
                if attrs['password'] != attrs['confirm_password']:
                    raise serializers.ValidationError("Password is not match with confirm password")
                return attrs

    def to_representation(self, obj):
        returnObj = super(AccountSerializer, self).to_representation(obj)
        follower_count = len(followers(obj))
        print(follower_count)
        following_count = len(following(obj))
        total_posts = len(Topic.objects.filter(author = obj.id))
        new_obj = {}

        if self.context['request'].user.id == obj.id:
            new_obj["email"] = obj.email
        new_obj.update({
            "following": following_count,
            "follower": 0,
            "total_posts": total_posts,
            "am_I_following": is_following(self.context['request'].user, obj)})
        returnObj.update(new_obj)
        return returnObj

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name',instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.lastname)
        instance.pic = validated_data_get('pic', instance.pic)
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

    class Meta:
        model = User
        fields = ('id', 'username', 'image', 'full_name')
        read_only_fields = ('id', 'username')

    def to_preresentation(self, obj):
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


class IconSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = Icon
        fields = '__all__'
