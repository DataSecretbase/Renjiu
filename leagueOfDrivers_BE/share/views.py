from django.shortcuts import render
<<<<<<< HEAD
<<<<<<< HEAD
from wx_league import models as wx_league
=======
from django.db.models import Q
>>>>>>> 9505a7a53ebd8f7d43821ba97794df498552449b
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse
from rest_framework import permissions, status, views, viewsets
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from utils import auth
from wx_league import models as wx_league
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

<<<<<<< HEAD
    @list_route(methods=['get'])
    def add(self, request):
        return self.create(request)
=======
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
>>>>>>> f732481b08b46fe49ae469347944bf5ec8ca3422
=======
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
>>>>>>> 9505a7a53ebd8f7d43821ba97794df498552449b
