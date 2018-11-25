from django.shortcuts import render
from wx_league import models as wx_league
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse
from rest_framework import permissions, status, views, viewsets
from rest_framework.decorators import list_route, detail_route
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
    queryset = Cash.objects.all()
    def get_queryset(self):
        return ShareUser.objects.all()

    def create(self, request, pk=None):
        shareuser = self.get_object()
        shareuser = Cash.objects.create(user=shareuser,cash=0)
        serializer = self.serializer_class(shareuser, data=request.data)
        if serializer.is_valid():
            shareuser.price = serializer.validated_data.get("cash", 0)
            shareuser.save()
            return Response({
                'cash': serializer.data,
            }, status=status.HTTP_201_CREATED)
        return Response({
            'status': 'Bad request',
            'message': 'User could not be created with received data.',
            'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['post'])
    def add(self, request, pk=None):
        return self.create(request, pk)

    @detail_route(method=['get'])
    def list(self, request, pk=None):
        shareuser = self.get_object()
        cash_list = Cash.objects.filter(user=shareuser)
        serializer = CashListSerializer(cash_list)
        if serializer.is_valid():
            return Reponse({
                'cash_list': serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            'status': 'Bad request',
            'message': 'Cash list could not be search with received data.',
            'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)