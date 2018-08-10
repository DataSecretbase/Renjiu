from django.conf.urls import include, url
from . import views

urlpatterns = [

    url('^notice/list/$', views.notice_list, name='datein'),
    url('^discounts/coupons/$', views.discounts_coupons, name='datein'),
    url('^discounts/fetch/$', views.discounts_fetch, name='datein'),
    url('^banner/list/$', views.banner_list, name='datein'),
    url('^shop/goods/category/all$', views.category, name='datein'),
    url('^config/get-value$', views.get_value, name='datein'),
    url('^user/check-token$', views.check_token, name='datein'),
    url('^user/check-token$', views.check_token, name='datein'),
    url('^user/login$', views.verify, name='datein'),
    url('^address$', views.address, name='datein'),
    url('^address/detail$', views.address_detail, name='datein'),
    url('^address/list$', views.address_list, name='datein'),
    url('^address/delete$', views.address_delete, name='datein'),
    url('^goods/list$', views.goods_list, name='datein'),
    url('^goods/detail$', views.goods_detail, name='datein'),

]
