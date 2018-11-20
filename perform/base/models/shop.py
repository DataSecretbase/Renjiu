from django.db import models
from django.contrib.auth.models import AbstractUser
import django.utils.timezone as timezone
import random
import time
from uuid import uuid4
from datetime import datetime,date

#from .datasettings import league_model as m_set

from .user import Icon


class Shop(models.Model):
    province_id = models.IntegerField(verbose_name = '省', default = 0)
    #PROVINCE = ((0,'beijin'),)
    #CITY = ((0,'beijin'),(1,"shanghai"))
    city_id = models.IntegerField(verbose_name = '城市', default = 0)
    #DISTRICT = ((0,'beijin'))
    district_id = models.IntegerField(verbose_name = '区', default = 0)
    name = models.CharField(verbose_name = '店铺名称', max_length = 30)
    address = models.CharField(verbose_name='地址',
                               max_length=100,
                               blank = True,
                               null = True)
    phone = models.CharField(verbose_name = '联系电话',
                             max_length=50,
                             blank = True,
                             null = True)
    introduce = models.TextField(verbose_name='介绍')
    characteristic = models.TextField(verbose_name = '特色')
    sort = models.IntegerField(verbose_name = '排序')
    pic = models.ForeignKey('Icon',
                            verbose_name='店铺商标',
                            on_delete = models.SET_NULL, blank = True, null = True)
    activity = models.CharField(verbose_name = '打折优惠信息', max_length=255)
    latitude = models.FloatField(verbose_name = '纬度')
    longitude = models.FloatField(verbose_name = '经度')
    number_good_reputation = models.IntegerField(verbose_name = '好评数')
    number_order = models.IntegerField(verbose_name = '订单数')

    class Meta:
        db_table = 'Shop'
        verbose_name = '商店'
        verbose_name_plural = '商店'
        _order = 'sort'

    def __str__(self):
        return self.name
    
    def natural_key(self):
        return self.name
