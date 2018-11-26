from django.core.validators import validate_email

from rest_framework import serializers, validators

from .models import *
from base import serializers as base_serializers

class TopicSerializer(serializers.ModelSerializer):
    pic_index = base_serializers.IconSerializer(read_only = True)

    class Meta:
        model = Topic
        fields = ("__all__")

class IndexTopicSerializer(serializers.ModelSerializer):
    topic = TopicSerializer(read_only = True)


    class Meta:
        model = IndexTopic
        fields = ("id","topic")
