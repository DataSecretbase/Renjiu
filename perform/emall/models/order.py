from django.db import models
from django.contrib.auth.models import AbstractUser
import django.utils.timezone as timezone
import random
import time
from uuid import uuid4
from datetime import datetime,date

import base.models as base


class Order(models.Model):
    user = models.ForeignKey('base.User',
                                       verbose_name ='微信用户',
                                       on_delete = models.DO_NOTHING)
    number_goods = models.IntegerField(verbose_name = '商品数量',default = 0)
    goods_price = models.FloatField(verbose_name = '商品总金额', default=0)
    coupons_id = models.IntegerField(verbose_name = '使用的优惠券id', default=0)
    total = models.FloatField('实际支付', default=0 )
    ORDER_STATUS = [(0,"待付款"),(1,'待发货'),
                    (2,'待收货'),(3,'待评价'),
                    (4,'已完成'),(5,'已删除')]
    status = models.SmallIntegerField(verbose_name = '状态',
                                      choices = ORDER_STATUS,
                                      default = 0)
    remark = models.CharField(verbose_name  = '备注', max_length = 100, blank = True)
    linkman = models.CharField(verbose_name = '联系人', max_length = 100, blank = True)
    phone = models.CharField(verbose_name = '手机号码', max_length = 50, blank = True)
    #PROVINCE = ((0,"22"))
    province_id = models.SmallIntegerField(verbose_name='省', default = 0)
    #CITY = ((0,"22"))
    city_id = models.SmallIntegerField(verbose_name = '市', default = 0)
    district_id = models.SmallIntegerField(verbose_name = '区', default = 0)
    address = models.CharField(verbose_name = '详细地址', max_length = 100, blank = True)
    postcode = models.CharField(verbose_name = '邮政编码', max_length = 20, blank = True)
    #display_traces = fields.Html('物流信息', compute='_compute_display_traces')
    traces = models.TextField(verbose_name = '物流信息', blank = True)
    date_add = models.DateTimeField(verbose_name = '下单时间',
                                   default = timezone.now)

    class Meta:
        db_table = 'Order'
        verbose_name = '订单'
        verbose_name_plural = '订单'
 
    #payment_ids = fields.One2many('wechat_mall.payment', 'order_id', '支付记录')
    def __str__(self):
        return "{0}".format(self.id)


class OrderGoods(models.Model):
    order_id = models.ForeignKey('Order', verbose_name='订单', on_delete = models.SET_NULL,
            null = True, blank = True)
    # 冗余记录商品，防止商品删除后订单数据不完整
    goods_id = models.IntegerField(verbose_name = '商品id',default = 0)
    name = models.CharField(verbose_name = '商品名称',
                            max_length = 50,
                            blank =True)
    display_pic = models.ForeignKey('base.Icon',
                                    verbose_name = '图片',
                                    on_delete = models.SET_NULL,
                                    null = True,
                                    blank = True)
    property_str = models.CharField(verbose_name = '商品规格',
                                    max_length = 200,
                                    blank = True)
    price = models.FloatField(verbose_name = '单价', default = 0)
    amount = models.IntegerField(verbose_name = '商品数量', default = 0)
    total = models.FloatField(verbose_name = '总价', default = 0)
    
    class Meta:
        db_table = 'OrderGoods'
        verbose_name = '订单商品'
        verbose_name_plural = '订单商品'

    def __str__(self):
        return self.name


class Logistics(models.Model):
    name = models.CharField('名称', max_length = 50)
    by_self = models.BooleanField(verbose_name = '商家配送', default = False)
    free = models.BooleanField(verbose_name = '是否包邮', default = False)
    #LogisticsValuationType = ((0,"22"))
    valuation_type = models.SmallIntegerField(verbose_name='计价方式'
                                      ,default=0)

    class Meta:
        db_table = 'Logistics'
        verbose_name = '物流信息'
        verbose_name_plural = '物流信息'
    
    def __str__(self):
        return self.name

    def natural_key(self):
        return {"id":self.id,
                "name":self.name,
                "by_self":self.name,
                "free":self.free,
                "valuation_type":self.valuation_type}


class Shipper(models.Model):
    name =  models.CharField(verbose_name = '名称', max_length = 50)
    code = models.CharField(verbose_name = '编码', max_length = 100)

    class Meta:
        db_table = 'Shipper'
        verbose_name = '承运商'
        verbose_name_plural = '承运商'

    def __str__(self):
        return self.name

    def natural_key(self):
        return {"id":self.id,
                "name":self.name,
                "code":self.code}


class OrderGoods(models.Model):
    order_id = models.IntegerField(verbose_name='订单', default = 0)
    # 冗余记录商品，防止商品删除后订单数据不完整
    goods_id = models.IntegerField(verbose_name = '商品id',default = 0)
    name = models.CharField(verbose_name = '商品名称',
                            max_length = 50,
                            blank =True)
    display_pic = models.ForeignKey('base.Icon',
                                    verbose_name = '图片',
                                    on_delete = models.SET_DEFAULT,
                                    default = 0)
    property_str = models.CharField(verbose_name = '商品规格',
                                    max_length = 200,
                                    blank = True)
    price = models.FloatField(verbose_name = '单价', default = 0)
    amount = models.IntegerField(verbose_name = '商品数量', default = 0)
    total = models.FloatField(verbose_name = '总价', default = 0)
    
    class Meta:
        db_table = 'OrderGoods'
        verbose_name = '订单商品'
        verbose_name_plural = '订单商品'

    def __str__(self):
        return self.name



class DeliverWizard(models.Model):
    _name = 'wechat_mall.deliver.wizard'
    order_id = models.ForeignKey('Order',
                                 verbose_name='订单',
                                 on_delete = models.CASCADE)
    shipper_id = models.ForeignKey('Shipper',
                                   verbose_name='快递承运商',
                                   on_delete = models.CASCADE)
    tracking_number = models.CharField(verbose_name = '运单号', max_length = 200)
    status = models.CharField(verbose_name = '状态', max_length = 20)

    class Meta:
        db_table = 'DeliverWizard'
        verbose_name = '发货信息'
        verbose_name_plural = '发货信息'

    def natural_key(self):
        return {"id":self.id,
                "order_id":self.order_id,
                "shipper_id":self.shipper_id,
                "tracking_number":self.tracking_number,
                "status":self.status}
