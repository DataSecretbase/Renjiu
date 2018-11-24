from django.db import models
from django.contrib.auth.models import AbstractUser

import django.utils.timezone as timezone
import random
import time
from uuid import uuid4
from datetime import datetime,date

from .datasettings import league_model as m_set


class Goods(models.Model):
    category_id = models.ForeignKey('Category',
                                    on_delete=models.SET_DEFAULT,
                                    default=0)
    characteristic = models.CharField(verbose_name="描述",
                                      max_length=100,
                                      default='')
    date_add = models.DateTimeField(verbose_name='上架时间', auto_now_add=True)
    date_start = models.DateTimeField(verbose_name='上架时间', auto_now_add=True)
    date_update = models.DateTimeField(verbose_name='更新时间', auto_now=True)
    logistics_id = models.IntegerField(verbose_name='物流id', default=0)
    min_score = models.SmallIntegerField(verbose_name='最小评分', default=0)
    name = models.CharField(verbose_name='名称', max_length=60)
    number_fav = models.IntegerField(verbose_name="收藏人数", default=0)
    number_good_reputation = models.IntegerField(verbose_name="好评数量", default=0)
    number_orders = models.IntegerField(verbose_name='已售数量', default=0)
    original_price = models.FloatField(verbose_name="原价")
    paixu = models.IntegerField(default=0)
    pic = models.ForeignKey('Icon',
                            verbose_name="商品图片连接",
                            on_delete=models.SET_DEFAULT,
                            default=0)
    pingtuan = models.BooleanField(verbose_name="拼团", default=False)
    recommend_status = models.SmallIntegerField(verbose_name="推荐状态", default=0)
    shop_id = models.ForeignKey("DriverSchool",
                                verbose_name="商店id",
                                on_delete=models.CASCADE)
    status = models.SmallIntegerField(verbose_name="商品状态", default=0)
    stores = models.IntegerField(verbose_name="库存")
    video_id = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    weight = models.FloatField(default=0.00)

    class Meta:
        verbose_name = '商品'
        verbose_name_plural = '商品'

    def __str__(self):
        return self.name

    def natural_key(self):
        return {"id": self.id,
                "characteristic": self.characteristic,
                "date_add": self.date_add,
                "date_start": self.date_start,
                "date_update": self.date_update,
                "logistics_id": self.logistics_id,
                "min_score": self.min_score,
                "name": self.name,
                "number_fav": self.number_fav,
                "number_good_reputation": self.number_good_reputation,
                "numberOrders": self.number_orders,
                "original_price": self.original_price,
                "paixu": self.paixu,
                "pingtuan": self.pingtuan,
                "recommend_status": self.recommend_status,
                "status": self.status,
                "stores": self.stores,
                "video_id": self.video_id,
                "views": self.views,
                "weight": self.weight}


class Order(models.Model):
    wechat_user_id = models.ForeignKey('WechatUser',
                                       verbose_name='微信用户',
                                       on_delete=models.DO_NOTHING)
    number_goods = models.IntegerField(verbose_name='商品数量', default=0)
    goods_price = models.FloatField(verbose_name='商品总金额', default=0)
    coupons_id = models.IntegerField(verbose_name='使用的优惠券id', default=0)
    logistics_id = models.ForeignKey('Logistics',
                                     verbose_name='物流id',
                                     on_delete=models.SET_DEFAULT,
                                     default=0)
    logistics_price = models.FloatField(verbose_name='物流费用', default=0)
    total = models.FloatField('实际支付', default=0)
    ORDER_STATUS = [(0, "待付款"), (1, '待发货'),
                    (2, '待收货'), (3, '待评价'),
                    (4, '已完成'), (5, '已删除')]
    status = models.SmallIntegerField(verbose_name='状态',
                                      choices=ORDER_STATUS,
                                      default=0)
    remark = models.CharField(verbose_name='备注', max_length=100, blank=True)
    linkman = models.CharField(verbose_name='联系人', max_length=100, blank=True)
    phone = models.CharField(verbose_name='手机号码', max_length=50, blank=True)
    # PROVINCE = ((0,"22"))
    province_id = models.SmallIntegerField(verbose_name='省', default=0)
    # CITY = ((0,"22"))
    city_id = models.SmallIntegerField(verbose_name='市', default=0)
    district_id = models.SmallIntegerField(verbose_name='区', default=0)
    address = models.CharField(verbose_name='详细地址', max_length=100, blank=True)
    postcode = models.CharField(verbose_name='邮政编码', max_length=20, blank=True)
    shipper_id = models.ForeignKey('Shipper',
                                   verbose_name='快递承运商',
                                   on_delete=models.DO_NOTHING,
                                   default=1)
    tracking_number = models.CharField(verbose_name='运单号',
                                       max_length=200,
                                       blank=True)
    # display_traces = fields.Html('物流信息', compute='_compute_display_traces')
    traces = models.TextField(verbose_name='物流信息', blank=True)
    date_add = models.DateTimeField(verbose_name='下单时间',
                                    default=timezone.now)

    class Meta:
        db_table = 'Order'
        verbose_name = '订单'
        verbose_name_plural = '订单'

    # payment_ids = fields.One2many('wechat_mall.payment', 'order_id', '支付记录')
    def __str__(self):
        return "{0}".format(self.id)


class OrderGoods(models.Model):
    order_id = models.IntegerField(verbose_name='订单', default=0)
    # 冗余记录商品，防止商品删除后订单数据不完整
    goods_id = models.IntegerField(verbose_name='商品id', default=0)
    name = models.CharField(verbose_name='商品名称',
                            max_length=50,
                            blank=True)
    display_pic = models.ForeignKey('Icon',
                                    verbose_name='图片',
                                    on_delete=models.SET_DEFAULT,
                                    default=0)
    property_str = models.CharField(verbose_name='商品规格',
                                    max_length=200,
                                    blank=True)
    price = models.FloatField(verbose_name='单价', default=0)
    amount = models.IntegerField(verbose_name='商品数量', default=0)
    total = models.FloatField(verbose_name='总价', default=0)

    class Meta:
        db_table = 'OrderGoods'
        verbose_name = '订单商品'
        verbose_name_plural = '订单商品'

    def __str__(self):
        return self.name
