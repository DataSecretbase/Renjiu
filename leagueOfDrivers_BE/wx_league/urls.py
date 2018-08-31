from django.conf.urls import include, url
from . import views

urlpatterns = [

    url('^notice/list/$', views.notice_list, name='datein'),
    url('^discounts/coupons/$', views.discounts_coupons, name='datein'),
    url('^discounts/fetch/$', views.discounts_fetch, name='datein'),
    url('^banner/list/$', views.banner_list, name='datein'),
    url('^check/user$', views.check_cookies, name='datein'),
    url('^user/login$', views.verify, name='datein'),
    url('^address$', views.address, name='datein'),
    url('^address/detail$', views.address_detail, name='datein'),
    url('^address/list$', views.address_list, name='datein'),
    url('^address/delete$', views.address_delete, name='datein'),
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
    
]
