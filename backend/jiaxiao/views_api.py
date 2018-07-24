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

class UserFollowersViewSet(viewsets.ReadOnlyModelViewSet):
	serializer_class = AccountSerializer

	def get_queryset(self):
		user_id = self.kwargs['userid']
		user = User.objects.get(id = user_id)
		return following(user)

class ActivityViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = Action.objects.all()
	serializer_class = ActionSerializer
	
	filter_fields = (
		'actor_content_type', 'actor_content_type_model',
		'target_content_type', 'target_conent_type_model',
		'action_object_content_type', 'action_object_content_type_i_model',
	)

class AccountViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = AccountSerializer

	def get_queryset(self):
		if self.request.query_params.get("search",None):
			parmas = self.request.query_parmas.get("search", None)
			return User.objects.fillter(Q(username__icontatains = params)|
							Q(major__icontains = params)|
							Q(first_name__icontains = params)
							)

