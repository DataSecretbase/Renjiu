from django.conf.urls import include, url
from rest_framework_nested import routers

from .views import TopicViewSet, IndexTopicViewSet

router = routers.SimpleRouter()

router.register(r'Topic', TopicViewSet, base_name = 'topic')
router.register(r'IndexTopic', IndexTopicViewSet, base_name = 'indextopic')

urlpatterns = [
        url(r'', include(router.urls)),
        ]
