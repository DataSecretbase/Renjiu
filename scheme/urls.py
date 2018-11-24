from django.conf.urls import include, url
from rest_framework_nested import routers

from .views import SchemeViewSet

router = routers.SimpleRouter()

router.register(r'Scheme', SchemeViewSet, base_name = 'scheme')

urlpatterns = [
        url(r'', include(router.urls)),
        ]
