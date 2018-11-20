from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorations import detail_route

from .models import *
from wx_league import models as wx_league
from serializers import *

# Create your views here.

class UserShareCreateViewSet(viewsets.ModelViewSet):
    serializer_class = UserShareCreateSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            ShareUser.objects.create(user = WechatUser.objects.get(cookie = request.data.get("cookie", None)))
            return Response({
                    "status":"regist success!",
                }, status=status.HTTP_201_CREATED)
