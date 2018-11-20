from django.conf.urls import include, url
from rest_framework_nested import routers

from .views import GoodsViewSet, PreferentialViewSet, CategoryViewSet

router = routers.SimpleRouter()

router.register(r'Goods', GoodsViewSet, base_name = 'goods')
router.register(r'Preferential', PreferentialViewSet, base_name = 'preferential')
router.register(r'Category', CategoryViewSet, base_name = 'category')

urlpatterns = [
        url(r'', include(router.urls)),
        ]
