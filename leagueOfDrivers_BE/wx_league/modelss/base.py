from django.db import models
from django.contrib.auth.models import AbstractUser

import django.utils.timezone as timezone
import random
import time
from uuid import uuid4
from datetime import datetime,date

from . import league_model as m_set

class WechatUser(AbstractUser):
    cookie = models.CharField('用户认证标识',max_length=100,
                              default='',blank=True)
    name = models.CharField(verbose_name='昵称',max_length=40,blank=True)
    openid = models.CharField(verbose_name='OpenId',max_length=255,blank=True)
    union_id = models.CharField(verbose_name='UnionId',max_length=255,blank=True)
    gender = models.SmallIntegerField(verbose_name='gender',default=0,blank=True)
    language = models.CharField(verbose_name='语言',max_length=40,blank=True)
    user_type = models.SmallIntegerField(verbose_name='用户类型',choices=m_set.USER_TYPE,default=0)
    register_type = models.SmallIntegerField(verbose_name='注册来源',default=0)
    phone = models.CharField(verbose_name='手机号码',max_length=50,blank=True)
    country = models.IntegerField(verbose_name='国家',default=0,blank=True)((0,"beijin"))
    province = models.IntegerField(verbose_name='省份', default=0)
    city = models.IntegerField(verbose_name='城市', default=0)
    avatar = models.ForeignKey('Icon',verbose_name='头像',on_delete=models.SET_DEFAULT, default=0)
    register_ip = models.CharField(verbose_name='注册IP',max_length=80,blank=True)
    ip = models.CharField(verbose_name='登陆IP',max_length=80,blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'WechatUser'
        verbose_name = '微信用户'
        verbose_name_plural = '微信用户'

    def natural_key(self):
        return {"url": "https://qgdxsw.com:8000" + self.avatar.display_pic.url,
                "name": self.name,
                "id": self.id}

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def get_address(self):
        return self.country


class DriverSchool(models.Model):
    province_id = models.IntegerField(verbose_name='省', default=0)
    # PROVINCE = ((0,'beijin'),)
    # CITY = ((0,'beijin'),(1,"shanghai"))
    city_id = models.IntegerField(verbose_name='城市', default=0)
    # DISTRICT = ((0,'beijin'))
    district_id = models.IntegerField(verbose_name='区', default=0)
    name = models.CharField(verbose_name='店铺名称', max_length=30)
    address = models.CharField(verbose_name='地址',
                               max_length=100,
                               blank=True,
                               null=True)
    phone = models.CharField(verbose_name='联系电话',
                             max_length=50,
                             blank=True,
                             null=True)
    introduce = models.TextField(verbose_name='驾校介绍')
    characteristic = models.TextField(verbose_name='驾校特色')
    sort = models.IntegerField(verbose_name='排序')
    pic = models.ForeignKey('Icon',
                            verbose_name='驾校商标',
                            on_delete=models.DO_NOTHING)
    activity = models.CharField(verbose_name='打折优惠信息', max_length=255)
    latitude = models.FloatField(verbose_name='纬度')
    longitude = models.FloatField(verbose_name='经度')
    number_good_reputation = models.IntegerField(verbose_name='好评数')
    number_order = models.IntegerField(verbose_name='订单数')

    class Meta:
        db_table = 'DriverSchool'
        verbose_name = '驾校'
        verbose_name_plural = '驾校'
        _order = 'sort'

    def __str__(self):
        return self.name

    def natural_key(self):
        return self.name