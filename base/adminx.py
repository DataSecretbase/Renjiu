from django.contrib import admin
from .models import *
import xadmin
import xadmin.views as views


class UserAdmin(object):
    list_display = ['id','username','first_name','last_name','image','date_joined','created_at','updated_at']
    search_fields = ['id','username','first_name','last_name']
    list_filter = ['username',]
    model_icon = 'fa fa-book'
    ordering = ['-id','-date_joined','updated_at']
    readonly_fields = ['username','first_name','last_name','image','date_joined','create_at','updated_at']


class IconAdmin(object):
    list_display = ['id','name','display_pic','date_add']
    search_fields = ['id','name',]
    model_icon = 'fa fa-book'
    ordering = ['-date_add']
    readonly_fields = ['date_add']

xadmin.site.register(Icon, IconAdmin)
