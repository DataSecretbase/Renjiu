from django.core.validators import validate_email

from rest_framework import serializers, validators

from .models import *
from base import serializers as base_serializers

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ("__all__")


class SchemeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Scheme
        fields = ("__all__")
