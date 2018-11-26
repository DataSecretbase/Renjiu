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
from .serializers import TopicSerializer, IndexTopicSerializer

class TopicViewSet(viewsets.ModelViewSet):
    serializer_class = TopicSerializer

    def get_queryset(self):
        print(self.request.query_params.get("sorting",None))
        sorting = self.request.query_params.get('sorting', None)
        if sorting == 'life':
            q = {}
            q["node"] = Node.objects.get(name = self.request.query_params.get("sorting_type", None)).id
            return Topic.objects.filter(**q).order_by("-created_on")


class IndexTopicViewSet(viewsets.ModelViewSet):
    serializer_class = IndexTopicSerializer

    def get_queryset(self):
        sorting = self.request.query_params.get("sorting", None)
        if sorting == 'index':
            return IndexTopic.sorted_objects.index()
