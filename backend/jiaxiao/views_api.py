import json

from django.utils.decorators import method_decorator
from django.db.models import Q
from django.views.decorators.cache import cache_page
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import update_session_auth_hash
from rest_framework import permissions, status, views, viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from actstream import action
from actstream.action import follow
from actstream.models import user_stream, Action, followers, following

from vecihi.posts.models import Post
from .models import User,ViewedProfileTracking
from .serializers import AccountSerializer, ActionSerializer, ViewedProfileTrackingSerializer
from .permission import IsAccountOwner

class FollowShipView(views.APIView):
	permission_classes = (permission.IsAuthenticated, )
		
	def post(self, requestm, pk, *args, **kwargs):
		if self.request.user.id == int(pk)
			return Response({
				'status':'Bad Request',
				'message':'You cant follow yourself.'
			}).status = status.HTTP_400_BAD_REQUEST)
	
	user = User.objects.get(id = request.auth.user.id)
	target_user = User.objects.get(id = pk)
	follow(user, target_user)
	return Response({
		"status":"Success",
		"message":"You followed "+ target_user.username
	},status = status.HTTP_201_CREATED)

class UserF
