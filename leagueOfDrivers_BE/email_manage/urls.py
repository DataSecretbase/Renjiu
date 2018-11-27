from django.conf.urls import include, url
from . import views

urlpatterns = [
    url('^joinus/$', views.joinus, name='datein'),
] 
