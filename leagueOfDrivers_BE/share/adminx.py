from django.contrib import admin
from .models import *
import xadmin
import xadmin.views as xviews


# Register your models here.

class ShareUserAdmin(object):
    list_display = ['id', 'user', 'first_leader', 'second_leader',
                    'third_leader', 'add_time']
    search_fields = ['id', 'user', 'first_leader', 'second_leader',
                    'third_leader']
    list_filter = ['id', 'add_time']
    model_icon = 'fa fa-book'
    ordering = ['-add_time']
    readonly_fields = ['id', 'user', 'first_leader', 'second_leader',
                    'third_leader', 'add_time']


class ShareUserProfileAdmin(object):
    list_display = ['id', 'user', 'total_price', 'price',
                    'cash_price', 'total_cash', 'order_money', 'un_pay']
    search_fields = ['id', 'user']
    list_filter = ['id', 'user', 'total_price', 'price',
                    'cash_price', 'total_cash', 'order_money', 'un_pay']
    model_icon = 'fa fa-book'
    ordering = ['-id']
    readonly_fields = ['id', 'user', 'total_price', 'price',
                    'cash_price', 'total_cash', 'order_money', 'un_pay']

class ShareGoodsAdmin(object):
    list_display = ['id', 'goods', 'share_times', 'sales_num',
                    'store', 'cash_scheme', 'add_time']
    search_fields = ['id', 'goods']
    list_filter = ['id', 'goods', 'share_times', 'sales_num',
                    'store', 'cash_scheme', 'add_time']
    model_icon = 'fa fa-book'
    ordering = ['-add_time']
    readonly_fields = ['id', 'goods', 'share_times', 'sales_num',
                    'store', 'cash_scheme', 'add_time']

class ShareOrderGoodsAdmin(object):
    list_display = ['id', 'order', 'sharegoods', 'name',
                    'display_pic', 'property_str', 'price','amount','total']
    search_fields = ['id', 'order', 'sharegoods', 'name']
    list_filter = ['id', 'order', 'sharegoods', 'name','price','total']
    model_icon = 'fa fa-book'
    ordering = ['-id']
    readonly_fields = ['id', 'order', 'sharegoods', 'name',
                    'display_pic', 'property_str', 'price','amount','total']

class RebateLogAdmin(object):
    list_display = ['id', 'user', 'buy_user', 'order',
                    'money', 'level', 'create_time','confirm',
                    'status','confirm_time','remark','store']
    search_fields = ['id', 'user', 'buy_user', 'order']
    list_filter = ['id','money', 'level', 'create_time','confirm',
                    'status','confirm_time','remark','store']
    model_icon = 'fa fa-book'
    ordering = ['-create_time']
    readonly_fields = ['id', 'user', 'buy_user', 'order',
                    'money', 'level', 'create_time','confirm',
                    'status','confirm_time','remark','store']

xadmin.site.register(RebateLog, RebateLogAdmin)
xadmin.site.register(ShareOrderGoods, ShareOrderGoodsAdmin)
xadmin.site.register(ShareGoods, ShareGoodsAdmin)
xadmin.site.register(ShareUserProfile, ShareUserProfileAdmin)
xadmin.site.register(ShareUser, ShareUserAdmin)