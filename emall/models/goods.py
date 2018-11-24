from django.db import models
from django.db.models import Count, Avg
from django.contrib.auth.models import AbstractUser
import django.utils.timezone as timezone
import random
import time
from uuid import uuid4
from datetime import datetime,date
import inspect

import base.models as base
import sys

from ezhiGo import settings
from .config import models_config as m_set
from .order import *

class GoodsQuerySet(models.QuerySet):
    def preferential(self, sorting_type):
        q = {}
        q['preferential_type'] = int(sorting_type)
        q['date_end__gte'] = timezone.now()
        q['date_create__lte'] = timezone.now()
        return self.filter(**q)

    def category(self, category_id):
        q={}
        q['category_id'] = int(category_id)
        return self.filter(**q)

class Preferential(models.Model):
    goods = models.ForeignKey('Goods',
            on_delete = models.SET_NULL, 
            blank = True, null = True)
    off = models.FloatField(verbose_name = '打折折扣')
    date_create = models.DateTimeField(verbose_name = '特价商品生效时间', auto_now_add = True)
    date_end = models.DateTimeField(verbose_name = '特价商品下架时间')
    preferential_type = models.SmallIntegerField(max_length = 50 ,choices = m_set.PREFERENTIAL_TYPE)
    sorted_objects = GoodsQuerySet.as_manager()

    def goods_info(self):
        return self.goods.natural_key()


class Goods(models.Model):
    category_id = models.ForeignKey('Category',
                                    on_delete = models.SET_NULL,
                                    blank = True, null = True)
    characteristic = models.CharField(verbose_name = "描述",
                                      max_length = 100,
                                      default = '')
    date_add = models.DateTimeField(verbose_name = '上架时间', auto_now_add = True)
    date_start = models.DateTimeField(verbose_name = '上架时间', auto_now_add = True)
    date_update = models.DateTimeField(verbose_name = '更新时间', auto_now = True)
    min_score = models.SmallIntegerField(verbose_name = '最小评分', default = 0)
    name = models.CharField(verbose_name = '名称', max_length = 60)
    number_good_reputation = models.IntegerField(verbose_name = "好评数量",default = 0)
    number_orders = models.IntegerField(verbose_name = '已售数量',default = 0)
    original_price = models.FloatField(verbose_name = "原价")
    pic = models.ForeignKey('base.Icon',
                            verbose_name = "商品图片连接",
                            on_delete = models.SET_NULL,
                            blank = True, null = True)
    pingtuan = models.BooleanField(verbose_name = "拼团" , default = False)
    recommend_status = models.SmallIntegerField(verbose_name = "推荐状态", default = 0)
    shop_id = models.ForeignKey("base.Shop",
                                verbose_name = "商店id",
                                on_delete = models.CASCADE)
    status = models.SmallIntegerField(verbose_name  = "商品状态", default = 0)
    stores = models.IntegerField(verbose_name = "库存")
    video_id = models.IntegerField(default = 0)
    views = models.IntegerField(default = 0)
    weight = models.FloatField(default = 0.00)
    sorted_objects = GoodsQuerySet.as_manager()

    class Meta:
        verbose_name = '商品'
        verbose_name_plural = '商品'

    def __str__(self):
        return self.name

    def natural_key(self):
        return {"id":self.id,
                "characteristic":self.characteristic,
                "date_add":self.date_add,
                "date_start":self.date_start,
                "date_update":self.date_update,
                "min_score":self.min_score,
                "name":self.name,
                "number_good_reputation":self.number_good_reputation,
                "numberOrders":self.number_orders,
                "original_price":self.original_price,
                "pic":settings.domain_url + self.pic.display_pic.url,
                "pingtuan":self.pingtuan,
                "recommend_status":self.recommend_status,
                "status":self.status,
                "stores":self.stores,
                "video_id":self.video_id,
                "views":self.views,
                "weight":self.weight}

class CategoryQuerySet(models.QuerySet):
    def index(self):
        q = {}
        q['sort'] = 0
        return self.all()


class Category(models.Model):
    name = models.CharField(verbose_name='名称', max_length = 100)
    eng_name = models.CharField(verbose_name = '名称(英文)', max_length = 100)
    category_type = models.CharField(verbose_name = '类型',max_length = 30)
    pid = models.ForeignKey('Category',
                            verbose_name='上级分类',
                            on_delete = models.SET_NULL,
                            blank = True, null = True)
    key = models.IntegerField(verbose_name='编号')
    icon = models.ForeignKey('base.Icon',
                             verbose_name='图标',
                             on_delete = models.SET_NULL,
                             blank = True, null = True)
    level = models.SmallIntegerField(verbose_name='分类级别')
    is_use = models.BooleanField(verbose_name='是否启用', default=True)
    sort = models.IntegerField(verbose_name='排序')
    sorted_objects = CategoryQuerySet.as_manager()
    
    class Meta:
        db_table = 'Category'
        verbose_name = '商品分类'
        verbose_name_plural = '商品分类'
        _order = 'level,sort'
    def __str__(self):
        return self.name


class ModifyPriceWizard(models.Model):
    order_id = models.ForeignKey('Order',
                                 verbose_name ='订单',
                                 on_delete = models.CASCADE)
    total = models.FloatField(verbose_name = '金额')

    class Meta:
        db_table = 'ModifyPriceWizard'
        verbose_name = '修改价格'
        verbose_name_plural = '修改价格'

    def natural_key(self):
        return {"id":self.id,
                "order_id":self.order_id,
                "total":self.total}




class GoodsReputation(models.Model):
    goods_id = models.ForeignKey('Goods',
                                 on_delete = models.SET_NULL,
                                 verbose_name = '商品',
                                 blank = True,
                                 null = True)
    user = models.ForeignKey('base.User',
                                on_delete = models.SET_NULL,
                                verbose_name = '评论用户',
                                blank = True,
                                null = True)
    goods_reputation_str = models.CharField(verbose_name = "评价级别",
                                            max_length = 20)
    goods_reputation_remark = models.TextField(verbose_name = "评论备注")
    dates_reputation = models.DateTimeField(verbose_name = "评论日期",
                                            auto_now_add = True)

    class Meta:
        db_table = 'GoodsReputation'
        verbose_name = '商品评论'
        verbose_name_plural = '商品评论'
    
    def __str__(self):
        return self.goods_id.name

    def natural_key(self):
        return {"id":self.id,
                "goods_id":self.user_id,
                "goods_reputation_str":self.goods_reputation_str,
                "goods_reputation_remark":self.goods_reputation_remark,
                "dates_reputation":self.dates_reputation}

