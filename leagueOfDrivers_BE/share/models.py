from django.db import models
from django.db.models import Count, Avg
import django.utils.timezone as timezone
import random
import time
from datetime import datetime, date

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


class ShareUserProfile(models.Model):
    user = models.ForeignKey(ShareUser, on_delete=models.CASCADE, verbose_name="用户分销详细资料",)
    total_price = models.FloatField(verbose_name="累计佣金", default=0)
    price = models.FloatField(verbose_name="可提现佣金", default=0)
    cash_price = models.FloatField(verbose_name="成功提现佣金", default=0)
    total_cash = models.FloatField(verbose_name="分销佣金", default=0)
    team_count = models.IntegerField(verbose_name="我的团队人数", default=0)
    order_money = models.FloatField(verbose_name="分销订单", default=0)
    un_pay = models.FloatField(verbose_name="分销订单", default=0)

    def share_qrcode(self):
        return settings.DOMAIN+"share_code/"+str(self.user.id)


class ShareGoods(models.Model):
    user = models.ForeignKey(wx_league.WechatUser, verbose_name='商品所属用户',
                             on_delete=models.SET_NULL, null=True, blank=True)
    goods = models.ForeignKey(wx_league.Goods, verbose_name='分销商品',
                              on_delete=models.SET_NULL, null=True, blank=True)
    share_times = models.IntegerField(verbose_name="分享次数")
    sales_num = models.IntegerField(verbose_name='分销销量')
    store = models.ForeignKey(wx_league.DriverSchool, verbose_name='商店',
                              on_delete=models.SET_NULL, null=True, blank=True)
    add_time = models.DateTimeField(verbose_name="加入分销时间", auto_now_add=True)


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
