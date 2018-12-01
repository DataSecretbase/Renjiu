from django.conf.urls import include, url
from . import views
from rest_framework_nested import routers

router = routers.SimpleRouter()

router.register(r'ShareUserProfile', views.ShareUserProfileViewSet,
                base_name='profile_shareuser')
router.register(r'Cash', views.CashViewSet,
                base_name='Cash')
router.register(r'ShareUser', views.ShareUserViewSet,
                base_name='ShareUser')
router.register(r'ShareOrder', views.ShareOrderViewSet,
                base_name='ShareOrder')

urlpatterns = [
    url(r'', include(router.urls)),
    url('^isshareuser/$', views.is_shareuser, name='is_shareuser'),
]