from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import detail_route
from actstream import action
# Create your views here.

from .models import *

from base.models import User
from .permissions import IsAuthor, IsOwner
from .serializers import GoodsSerializer, CategorySerializer, \
                GoodsReputationSerializer, PreferentialSerializer,\
                OrderSerializer

class PreferentialViewSet(viewsets.ModelViewSet):
    serializer_class = PreferentialSerializer

    def get_queryset(self):
        sorting = self.request.query_params.get('sorting', None)
        if sorting == 'preferential': #限时特惠
            sorting_type = self.request.query_params.get('sorting_type', None)
            return Preferential.sorted_objects.preferential(sorting_type)


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer

    def get_queryset(self):
        sorting = self.request.query_params.get('sorting', None)
        if sorting == 'index': #首页分类
            return Category.sorted_objects.index()


class GoodsViewSet(viewsets.ModelViewSet):
    serializer_class = GoodsSerializer

    def get_queryset(self):
        sorting = self.request.query_params.get('sorting', None)
        if sorting == 'preferential':  #限时特惠
            print("prefer")
            return Preferential.sorted_objects.preferential()
        if sorting == 'inventory':  #清仓更替
            return Goods.sorted_objects.inventory()
        if sorting == 'offers':  #特价
            return Goods.sorted_objects.offers()

        if sorting == 'category':
            category = self.request.query_params.get('category_id', None)
            return Goods.sorted_objects.category(category)

    @method_decorator(cache_page(60))
    def dispatch(self, *args, **kwargs):
        return super(GoodsViewSet, self).dispatch(*args, **kwargs)

    @detail_route(methods = ['post'], permission_classes=[permissions.IsAuthenticated])
    def purchase(self, request, pk=None):
        if not(isinstance(int(request.data.get("goods_num")),int) and int(request.data.get("goods_num")) > 0):
            return Response({
                    'staus': 'Not Found',
                    'message': 'goods_num field is invalidated'
                }, status = status.HTTP_400_BAD_REQUEST)
            serializer = GoodsPurcharSerializer(
                    data = {
                        'goods':pk,
                        'goods_num':request.data["goods_num"],
                        'coupon':request.data["coupon"]
                        },
                    context = {'request':request})
            if serizliser.is_valid():
                serializer.save()
                goods = Goods.objects.get(pk=pk)
                return Response(GoodsSerializer(goods, context={'request': request}).data)
            else:
                return Response(serializer.errors,
                        status = status.HTTP_400_BAD_REQUEST)


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer

    @detail_route(methods = ['post'], permission_class=[permissions.IsAuthenticated])
    def perform_create(self, serializer):
        instance = serializer.save(user=self.request.user)
        return super(OrderViewset, self).perform_create(serializer)



class OrderPaymentViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)
        return (permissions.IsAuthenticated(), IsOwner(),)

    def perform_create(self, serializer):
        instance = serializer.save(user = self.request.user)
        return super(PostUpvoteViewSet, self).perform_create(serializer)
