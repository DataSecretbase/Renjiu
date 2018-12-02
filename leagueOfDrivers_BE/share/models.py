from django.db import models
from django.db.models import Count, Avg
import django.utils.timezone as timezone
import random
import time
from datetime import datetime, date
from django.db.models import Q

import wx_league.models as wx_league

from .config import models_set
from leagueOfDrivers import settings

# Create your models here.


class ShareUser(models.Model):
    user = models.OneToOneField(wx_league.WechatUser, related_name="share_user",
                                verbose_name="分销用户", on_delete=models.CASCADE)
    first_leader = models.ForeignKey(wx_league.WechatUser, related_name="share_f_leader",
                                     verbose_name="第一个上级", on_delete=models.SET_NULL,
                                     null=True, blank=True)
    second_leader = models.ForeignKey(wx_league.WechatUser, related_name="share_s_leader",
                                      verbose_name='第二个上级', on_delete=models.SET_NULL,
                                      null=True, blank=True)
    third_leader = models.ForeignKey(wx_league.WechatUser, related_name="share_t_leader",
                                     verbose_name='第三个上级', on_delete=models.SET_NULL,
                                     null=True, blank=True)
    add_time = models.DateField(verbose_name="注册时间", auto_now_add=True)


class ShareUserProfile(models.Model):
    user = models.ForeignKey(ShareUser, on_delete=models.CASCADE, verbose_name="用户分销详细资料",)
    total_price = models.FloatField(verbose_name="累计佣金", default=0)
    price = models.FloatField(verbose_name="可提现佣金", default=0)
    cash_price = models.FloatField(verbose_name="成功提现佣金", default=0)
    total_cash = models.FloatField(verbose_name="分销佣金", default=0)
    order_money = models.FloatField(verbose_name="分销订单", default=0)
    un_pay = models.FloatField(verbose_name="分销订单", default=0)

    def share_qrcode(self):
        return settings.DOMAIN+"share_code/"+str(self.user.id)

    def team_count(self):
        return len(ShareUser.objects.filter(Q(first_leader=self.user.user)|
                                 Q(second_leader=self.user.user)|
                                 Q(third_leader=self.user.user)))


class ShareGoods(models.Model):
    user = models.ForeignKey(wx_league.WechatUser, verbose_name='商品所属用户',
                             on_delete=models.SET_NULL, null=True, blank=True)
    goods = models.ForeignKey(wx_league.Goods, verbose_name='分销商品',
                              on_delete=models.SET_NULL, null=True, blank=True)
    share_times = models.IntegerField(verbose_name="分享次数")
    sales_num = models.IntegerField(verbose_name='分销销量')
    store = models.ForeignKey(wx_league.DriverSchool, verbose_name='分销商',
                              on_delete=models.SET_NULL, null=True, blank=True)
    cash_scheme = models.SmallIntegerField(choices=models_set.CASH_SCHEME, default=0)
    add_time = models.DateTimeField(verbose_name="加入分销时间", auto_now_add=True)


class ShareOrderGoods(models.Model):
    order = models.ForeignKey('wx_league.Order', verbose_name='订单',
                              on_delete=models.SET_NULL, null=True, blank=True)
    # 冗余记录商品，防止商品删除后订单数据不完整
    # 分销商品 数据关联 本app的Sharegoods
    sharegoods = models.ForeignKey('ShareGoods', verbose_name='分销商品',
                                   on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(verbose_name='商品名称', max_length=50, blank=True)
    display_pic = models.ForeignKey('wx_league.Icon', verbose_name='图片',
                                    on_delete=models.SET_DEFAULT, default=0)
    property_str = models.CharField(verbose_name='商品规格', max_length=200, blank=True)
    price = models.FloatField(verbose_name='单价', default=0)
    amount = models.IntegerField(verbose_name='商品数量', default=0)
    total = models.FloatField(verbose_name='总价', default=0)

    class Meta:
        db_table = 'ShareOrderGoods'
        verbose_name = '订单商品'
        verbose_name_plural = '订单商品'


class RebateLog(models.Model):
    user = models.ForeignKey(wx_league.WechatUser, related_name="rebatelog_u",
                             verbose_name='获佣用户', on_delete=models.SET_NULL, null=True, blank=True)
    buy_user = models.ForeignKey(wx_league.WechatUser, related_name="rebatelog_buy_u",
                                 verbose_name='购买用户', on_delete=models.SET_NULL,
                                 null=True, blank=True)
    order = models.ForeignKey(wx_league.Order, verbose_name='订单',
                              related_name="rebatelog_o", on_delete=models.SET_NULL,
                              null=True, blank=True)
    money = models.FloatField(verbose_name="佣金")
    level = models.SmallIntegerField(verbose_name="获佣级别")
    create_time = models.DateTimeField(verbose_name="获得佣金时间", auto_now_add=True)
    confirm = models.DateTimeField(verbose_name="确认收钱时间", null=True, blank=True)
    status = models.SmallIntegerField(verbose_name='佣金状态', choices=models_set.REBATE_STATUS)
    confirm_time = models.DateTimeField(verbose_name='确认分成或者取消时间')
    remark = models.CharField(verbose_name="取消备注", max_length=200, null=True, blank=True)
    store = models.ForeignKey(wx_league.DriverSchool, verbose_name="店铺",
                              on_delete=models.SET_NULL, null=True, blank=True)


class Cash(models.Model):
    user = models.ForeignKey(ShareUser, on_delete=models.CASCADE, verbose_name="用户",)
    cash = models.FloatField(verbose_name="提现金额")
    add_time = models.DateTimeField(verbose_name="添加时间", auto_now_add=True)
    status = models.SmallIntegerField(verbose_name="提现状态", choices=models_set.CASH_STATUS, default=0)
