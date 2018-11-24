from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import detail_route

# Create your views here.

from .models import *
from .serializers import CategorySerializer, SchemeSerializer

class SchemeViewSet(viewsets.ModelViewSet):
    serializer_class = SchemeSerializer

    def get_queryset(self):
        sorting = self.request.query_params.get('sorting', None)
        if sorting == 'scheme': #一体方案
            q = {}
            q["category_id"] = Category.objects.get(\
                    name = self.request.query_params.get('sorting_type', None)).id
            return Scheme.objects.filter(**q).order_by("-date_create")
