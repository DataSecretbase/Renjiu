from django.conf.urls import include, url
from . import views
from rest_framework_nested import routers

from .views_api import AccountViewSet, LoginView, LogoutView, \
                            ActivityViewSet, FollowShipView, \
                             UserFollowersViewSet, UserFollowingViewSet


router = routers.SimpleRouter()
router.register(r'accounts', AccountViewSet)
router.register(r'accounts/(?P<userid>[0-9]+)/followers', UserFollowersViewSet, base_name='accounts')
router.register(r'accounts/(?P<userid>[0-9]+)/following', UserFollowingViewSet, base_name='accounts')
router.register(r'get-activity', ActivityViewSet, base_name='get-activity')



urlpatterns = [
    url(r'', include(router.urls)),
    url(r'follow/(?P<pk>[0-9]+)', FollowShipView.as_view(), name='follow'),
    url(r'auth/login/', LoginView.as_view(), name='login'),
    url(r'auth/logout/', LogoutView.as_view(), name='logout'),
    url('^notice/list/$', views.notice_list, name='notice'),
    url('^discounts/coupons/$', views.discounts_coupons, name='discounts_coupons'),
    url('^discounts/fetch/$', views.discounts_fetch, name='discounts_fetch'),
    url('^discounts/my$', views.discounts_fetch, name='discount_my'),
    url('^banner/list/$', views.banner_list, name='banner_list'),
    url('^check/user$', views.check_cookies, name='check_cookies'),
    url('^user/login$', views.verify, name='verify'),
    url('^address$', views.address, name='addres'),
    url('^address/detail$', views.address_detail, name='address_detail'),
    url('^address/list$', views.address_list, name='address_list'),
    url('^address/delete$', views.address_delete, name='address_delete'),
    url('^address/update$', views.address_update, name='datein'),
    url('^goods/list$', views.goods_list, name='datein'),
    url('^goods/detail$', views.goods_detail, name='datein'),
    url('^goods/price$', views.goods_price, name='datein'),
    url('^coupons$', views.coupons, name='datein'),
    url('^coupons/fetch$', views.coupons_fetch, name='datein'),
    url('^coupons/my$', views.coupons_my, name='datein'),
    url('^order/list$', views.order_list, name='datein'),
    url('^order/close$', views.order_close, name='datein'),
    url('^order/create$', views.order_create, name='datein'),
    url('^index/imageList$', views.index_imageList, name='datein'),
    url('^order/detail$', views.order_detail, name='datein'),
    url('^checkqr$', views.checkqr, name='datein'),
    url('^dateupdate$', views.datein, name='datein'),
    url('^school/detail$', views.school_detail, name='datein'),
    url('^email', views.send_email, name = 'datein'),
    url('^goods/reputation', views.goods_reputation, name = 'datein'),
    url('^bargain/detail', views.bargain_detail, name = 'datein'),
    url('^bargain/add', views.bargain_add, name = 'datein'),
    url('^isenrol', views.is_enrol, name = 'datein'),
    url('^coach/list', views.coach_list, name = 'datein'),
    url('^book/add', views.book_add, name = 'datein'),
    url('^booksets/add', views.booksets_add, name = 'datein'),
    url('^booksets/all', views.booksets_all, name = 'datein'),
    
]
