from django.conf.urls import include, url
from . import views

urlpatterns = [

    url('^notice/list/$', views.notice_list, name='datein'),
    url('^discounts/coupons/$', views.discounts_coupons, name='datein'),
    url('^discounts/fetch/$', views.discounts_fetch, name='datein'),
    url('^banner/list/$', views.banner_list, name='datein'),
    url('^user/check-token$', views.check_token, name='datein'),
    url('^user/check-token$', views.check_token, name='datein'),
    url('^user/login$', views.verify, name='datein'),
    url('^address$', views.address, name='datein'),
    url('^address/detail$', views.address_detail, name='datein'),
    url('^address/list$', views.address_list, name='datein'),
    url('^address/delete$', views.address_delete, name='datein'),
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

]
