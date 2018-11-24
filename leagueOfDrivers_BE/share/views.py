from django.shortcuts import render
from wx_league import models as wx_league
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse
from rest_framework import permissions, status, views, viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response
from utils import auth
from .models import *
from .serializers import *
# Create your views here.


def is_shareuser(request):
    cookie = request.GET.get("cookie")
    try:
        user = wx_league.WechatUser.objects.get(cookie=cookie)
        if len(ShareUser.objects.filter(user=user)) == 1:
            return JsonResponse({"code": 0, "status": "success"})
        else:
            return JsonResponse({"code": 400, "msg": "你还不是分销商"})
    except ObjectDoesNotExist:
        return JsonResponse({"code": 500, "msg": "你还未登录"})


class ShareUserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ShareUserProfileSerializer

    def get_queryset(self):
        cookie = self.request.query_params.get("cookie", None)
        if cookie is not None:
            return ShareUserProfile.objects.filter(
                user=ShareUser.objects.get(
                    user=wx_league.WechatUser.objects.get(cookie=cookie)))


class CashViewSet(viewsets.ModelViewSet):
    serializer_class = CashCreateSerializer

    def get_queryset(self):
        return Cash.objects.all()

    def create(self, request):
        print(request.GET)
        serializer = self.serializer_class(data = {}, cookie=request.GET.get("cookie",None), cash=request.GET.get("cash",None))
        if serializer.is_valid():
            Cash.objects.create(**serializer.validated_data)
            return Response({
                'account': serializer.data,
            }, status=status.HTTP_201_CREATED)
        return Response({
            'status': 'Bad request',
            'message': 'User could not be created with received data.',
            'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    @list_route(methods=['get'])
    def add(self, request):
        return self.create(request)