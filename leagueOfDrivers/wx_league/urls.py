from django.conf.urls import include, url
from . import views

urlpatterns = [

    url('^notice/list/$', views.notice_list, name='datein'),

]
