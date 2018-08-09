from rest_framework import serializers
from .models import *



class CouponsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Coupons
        fields = '__all__'

