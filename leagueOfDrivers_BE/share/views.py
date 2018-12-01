from django.shortcuts import render
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse
from rest_framework import permissions, status, views, viewsets
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from utils import auth
from wx_league import models as wx_league
from .models import *
from .serializers import *
# Create your views here.


def is_shareuser(request):
    token = request.GET.get("token")
    try:
        user = Token.objects.get(key=token)
        if len(ShareUser.objects.filter(user=user.user)) == 1:
            return JsonResponse({"code": 0, "status": "success"})
        else:
            return JsonResponse({"code": 400, "msg": "你还不是分销商"})
    except ObjectDoesNotExist:
        return JsonResponse({"code": 500, "msg": "你还未登录"})


class ShareUserViewSet(viewsets.ModelViewSet):
    queryset = ShareUser.objects.all()
    serializer_class = UserShareSerializer

    def get_queryset(self):
        token = self.request.query_params.get("token", None)
        if token is not None:
            account = Token.objects.get(key=token).user
            return ShareUser.objects.filter(Q(first_leader=account) |
                                            Q(second_leader=account) |
                                            Q(third_leader=account)
                                            )


    @detail_route(methods=['get'])
    def lists(self, request, pk=None):
        shareuser = wx_league.WechatUser.objects.get(pk=pk)
        print(shareuser)
        data=[]

        for x in [{"user":shareuser},{"first_leader":shareuser},{"second_leader":shareuser},{"third_leader":shareuser}]:
            team = ShareUser.objects.filter(**x)
            page = self.paginate_queryset(team)


            page = self.paginate_queryset(team)
            if page is not None:
                serializer = self.get_serializer(page,data=request.data, context={'request': request}, many=True)
                return self.get_paginated_response(serializer.data)
            elif len(team)==1:

                    serializer = self.get_serializer(team[0], data=request.data)
                    if serializer.is_valid():
                        data.append([serializer.data,])
                        continue
            else:
                serializer = self.get_serializer(team, many=True)

            data.append(serializer.data)

        return Response({
            'team': data,
        }, status=status.HTTP_200_OK)


class ShareUserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ShareUserProfileSerializer

    def get_queryset(self):
        token = self.request.query_params.get("token", None)
        if token is not None:
            return ShareUserProfile.objects.filter(
                user=ShareUser.objects.get(
                    user=Token.objects.get(key=token).user))


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
            if serializer.validated_data.get("cash", 0) <= 0:
                shareuser.status = 3
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

    @detail_route(methods=['get'])
    def lists(self, request, pk=None):
        shareuser = self.get_object()
        cash_list = Cash.objects.filter(user=shareuser).filter(~Q(status=3)).order_by('-add_time')
        page = self.paginate_queryset(cash_list)
        serializer = CashListSerializer(page if page else cash_list, data=request.data, many=True)
        if serializer.is_valid():
            return Response({
                'cash_list': serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            'status': 'Bad request',
            'message': 'Cash list could not be search with received data.',
            'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)