from django.contrib import admin
from .models import *
import xadmin
import xadmin.views as xviews
# Register your models here.

class DriverSchoolAdmin(object):
    """驾校"""
    
    list_display = ['id','province_id','city_id','district_id',
                    'name','address','phone','introduce',
                    'characteristic','sort','pic','activity',
                    'latitude','longitude','number_good_reputation','number_order']
    search_fields = ['id','province_id','city_id','district_id','name','phone']
    list_filter = ['introduce','characteristic']
    model_icon = 'fa fa-book'
    ordering = ['-id']
    readonly_fields = ['number_good_reputation','number_order']

xadmin.site.register(DriverSchool, DriverSchoolAdmin)


class BookSetAdmin(object):
    list_display = ['id','coach_driver_school','num_student','book_date_start',
                    'book_date_end','cur_book','status','set_type']
    search_fields = ['id','coach_driver_school','status','set_type']
    list_filter = ['coach_driver_school','num_student']
    model_icon = 'fa fa-book'
    ordering = ['-id','-book_date_start']
    readonly_fields = ['coach_driver_school','cur_book','status','set_type']

xadmin.site.register(BookSet,BookSetAdmin)


class CoachDriverSchoolAdmin(object):
    list_display = ['id','coach','train_ground']
    search_fields = ['id','coach','train_ground']
    list_filter = ['coach','train_ground']
    model_icon = 'fa fa-book'
    ordering = ['-id','-coach','-train_ground']
    readonly_fields = ['train_ground']

xadmin.site.register(CoachDriverSchool,CoachDriverSchoolAdmin)


class UserExamAdmin(object):
    list_display = ['id','user_id','exam_status','exam_type',
                    'exam_results','train_ground','date_add','date_end']
    search_fields = ['id','user_id','exam_status','train_ground']
    list_filter = ['id','exam_status']
    model_icon = 'fa fa-book'
    ordering = ['-id','-date_add']
    readonly_fields = ['user_id','exam_status','exam_type','train_ground','date_add','date_end']

xadmin.site.register(UserExam,UserExamAdmin)


class WechatUserAdmin(object):
    list_display = ['id','name','gender','user_type',
                    'register_type','phone','country','province',
                    'city','avatar','register_ip','ip']
    search_fields = ['id','name','gender','user_type','phone','province','city']
    list_filter = ['id','name','user_type']
    model_icon = 'fa fa-book'
    ordering = ['-id','-province','-city']
    readonly_fields = ['name','gender','user_type','register_type',
                       'phone','country','province','city',
                       'avatar','register_ip','ip']



class GoodsAdmin(object):
    list_display = ['id','category_id','characteristic','date_add',
                    'date_start','date_update','logistics_id','min_score',
                    'name','number_fav','number_good_reputation','number_orders',
                    'original_price','paixu','pic','pingtuan',
                    'recommend_status','shop_id','status','video_id',
                    'views','weight']
    search_fields = ['id','category_id','name','original_price']
    list_filter = ['date_add','date_start','date_update','logistics_id',
                   'minsocre','number_fav','number_good_reputation','number_orders',
                   'original_price','recommend_status','status']
    model_icon = 'fa fa-book'
    ordering = ['-id','-category_id','-date_add','-date_start',
                '-date_update','-logistics_id','-min_score','-number_fav',
                '-number_good_reputation','-number_orders','-original_price']
    readonly_fields = ['date_add','date_start','date_update','date_start','date_update','min_score','original_price','paixu','video_id','views','weight']

xadmin.site.register(Goods,GoodsAdmin)


class OrderAdmin(object):
    list_display = ['id','number_goods','goods_price','coupons_id',
                    'logistics_id','logistics_price','total','status',
                    'remark','linkman','phone','province_id',
                    'city_id','district_id','address','postcode',
                    'shipper_id','tracking_number','traces','date_add']
    search_fields = ['id','coupons_id','logistics_id','phone',
                     'province_id','city_id','district_id','tracking_number']
    list_filter = ['coupons_id','number_goods','goods_price','logistics_id',
                   'status','date_add']
    model_icon = 'fa fa-book'
    ordering = ['-id','-goods_price','-logitics_price','-total',
                '-province_id','-city_id','-district_id','-shipper_id']
    readonly_fields = ['number_goods','goods_price','coupons_id',
                    'logistics_id','logistics_price','total','status',
                    'remark','linkman','phone','province_id',
                    'city_id','district_id','address','postcode',
                    'shipper_id','tracking_number','traces','date_add']

xadmin.site.register(Order,OrderAdmin)


class OrderGoodsAdmin(object):
    list_display = ['id','order_id','goods_id','name',
                    'display_pic','property_str','price','amount','total']
    search_fields = ['id','order_id','goods_id','name']
    list_filter = ['order_id','goods_id','price','amount','total']
    model_icon = 'fa fa-book'
    ordering = ['-id','-order_id','-goods_id','-price','-amount','-total']
    readonly_fields = ['order_id','goods_id','name','display_pic','property_str','price','total']

xadmin.site.register(OrderGoods,OrderGoodsAdmin)


class ModifyPriceWizardAdmin(object):
    list_display = ['id','order_id','total']

xadmin.site.register(ModifyPriceWizard,ModifyPriceWizardAdmin)


class DeliverWizardAdmin(object):
    list_display = ['id','order_id','shipper_id','tracking_number','status']

xadmin.site.register(DeliverWizard,DeliverWizardAdmin)


class ShipperAdmin(object):
    list_display = ['id','name','code']
    
xadmin.site.register(Shipper,ShipperAdmin)


class LogisticsAdmin(object):
    list_display = ['id','name','by_self','free','valuation_type']

xadmin.site.register(Logistics,LogisticsAdmin)


class CategoryAdmin(object):
    list_display = ['id','name','eng_name','category_type',
                    'pid','key','icon','level',
                    'is_use','sort']
    search_fields = ['id','name','eng_name','category_type','pid','level']
    list_filter = ['category_type','pid','level','is_use']
    model_icon = 'fa fa-book'
    ordering = ['-category_type','pid','sort']
    readonly_fields = ['category_type']

xadmin.site.register(Category,CategoryAdmin)


