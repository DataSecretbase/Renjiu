from django.conf.urls import include, url
from . import views

urlpatterns = [

    url('^notice/list/$', views.notice_list, name='datein'),
    url('^discounts/coupons/$', views.discounts_coupons, name='datein'),
    url('^discounts/fetch/$', views.discounts_fetch, name='datein'),
    url('^banner/list/$', views.banner_list, name='datein'),

]
