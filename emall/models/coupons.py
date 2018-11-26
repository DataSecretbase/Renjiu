from django.db import models
import django.utils.timezone as timezone
import time
from datetime import datetime,date

from emall.utils import models_config as m_set
from base import models as base

class Coupons(models.Model):
    name = models.CharField(verbose_name = '优惠券名称', max_length = 50)
    money_min = models.FloatField(verbose_name = '优惠券金额')
    money_hreshold = models.FloatField(verbose_name = '满 减 最低额度')
    DATE_END_TYPE = ((0,"截止某日前有效"),(1,"领取后有效时间倒计"))
    date_end_type = models.SmallIntegerField(verbose_name = '优惠券有效期类型',
                                           choices = DATE_END_TYPE)
    date_end_days = models.DateTimeField(verbose_name = "优惠券截止时间",
                                       default = timezone.now)
    goods =  models.ForeignKey('Goods',
                                  on_delete = models.SET_NULL,
                                  null = True,
                                  blank = True,
                                  verbose_name = "商品id")
    is_active = models.BooleanField(verbose_name = "优惠券是否有效")
    date_add = models.DateTimeField(verbose_name = "优惠券添加的时间",
                                    default = timezone.now)
    coupons_type = models.SmallIntegerField(verbose_name = "优惠券类型1.通用型,2.分类专用型,3.商品专用型,4.店铺专用型",
                                       default = 0)


    class Meta:
        db_table = 'Coupons'
        verbose_name = '优惠券'
        verbose_name_plural = '优惠券'

        def __str__(self):
            return self.name


    def natural_key(self):
        return {"id":self.id,
                "name":self.name,
                "money_min":self.money_min,
                "money_hreshold":self.money_hreshold,
                "is_active":self.is_active,
                "date_add":self.date_add,
                "coupons_type":self.coupons_type}


class CouponsUser(models.Model):
    coupons = models.ForeignKey('Coupons',
                                   on_delete = models.SET_NULL,
                                   blank = True,
                                   null = True,
                                   verbose_name = "优惠券id")
    user = models.ForeignKey('base.User',
                                on_delete = models.SET_NULL,
                                blank = True,
                                null = True,
                                verbose_name = "用户id")
    date_add = models.DateTimeField(verbose_name = "优惠券添加的时间",
                                    default = timezone.now)
    date_end = models.DateTimeField(verbose_name = "优惠券截止时间",
                                       default = timezone.now)

    class Meta:
        db_table = 'Coupons_users'
        verbose_name = "用户领取的优惠券"
        verbose_name_plural = "用户领取的优惠券"

    def __str__(self):
        return self.coupons.name+self.user.name

    def natural_key(self):
        return {"id":self.id,
                "coupons":self.coupons,
                "user":self.user,
                "date_add":self.date_add,
                "date_end_days":self.date_end}


class Bargain(models.Model):
    goods = models.ForeignKey('Goods',
                                 on_delete = models.SET_NULL,
                                 null = True,
                                 blank = True,
                                 verbose_name = '货物')
    times = models.IntegerField(verbose_name = '砍价次数', default = 0)

    price = models.FloatField(verbose_name = '砍价当前价格')
    min_price = models.FloatField(verbose_name = '砍价最低价格')
    calculate_method = models.SmallIntegerField(verbose_name = '砍价计算模式',
                                                choices = m_set.BARGAIN_CALCULATE_METHOD)
    expected_price = models.FloatField(verbose_name = '期望砍价价格') 
    expected_times = models.FloatField(verbose_name = '期望砍价次数') 
    date_start = models.DateTimeField(verbose_name = '活动开始时间',
                                      auto_now_add = True)
    date_end = models.DateTimeField(verbose_name = '活动结束时间')

    class Meta:
        db_table = 'Bargain'
        verbose_name = '砍价'
        verbose_name_plural = '砍价'

    def __str__(self):
        return self.goods.name

    def natural_key(self):
        return {"id":self.id,
                "goods":self.goods.natural_key(),
                "times":self.times,
                "price":self.price,
                "min_price":self.min_price,
                "expected_price":self.expected_price,
                "expected_times":self.expected_times,
                "date_start":self.date_start,
                "date_end":self.date_end}


class BargainUser(models.Model):
    bargain = models.ForeignKey('Bargain',
                                   on_delete = models.SET_NULL,
                                   null = True,
                                   blank = True,
                                   verbose_name = '砍价活动')
    user = models.ForeignKey('base.User',
                                on_delete = models.SET_NULL,
                                null = True,
                                blank = True,
                                verbose_name = '砍价用户')
    bargain_date = models.DateTimeField(verbose_name = "砍价发起时间",
                                        auto_now_add = True)
    class Meta:
        db_table = 'BargainUser'
        verbose_name = '砍价用户记录'
        verbose_name_plural = '砍价用户记录'

    def __str__(self):
        return self.bargain.goods.name+self.user.name

    def natural_key(self):
        return {"id":self.id,
                "bargain":self.bargain.natural_key(),
                "user":self.user.natural_key()}


class BargainFriend(models.Model):
    bargain_user = models.ForeignKey('BargainUser',
                                       on_delete = models.SET_NULL,
                                       null = True,
                                       blank = True,
                                       verbose_name = '砍价发起用户')
    bargain_friend = models.ForeignKey('base.User',
                                         on_delete = models.SET_NULL,
                                         null = True,
                                         blank = True,
                                         verbose_name = '参与砍价好友')
    rank = models.IntegerField(verbose_name = "砍价次序")
    date_add = models.DateTimeField(verbose_name = '砍价时间',
                                   auto_now_add = True)
    class Meta:
        db_table = 'BargainFriend'
        verbose_name = '帮忙砍价的好友'
        verbose_name_plural = "帮忙砍价的好友"

    def __str__(self):
        return self.bargain_user.user.name+self.bargain_friend.name
 
    def natural_key(self):
        return {"id":self.id,
                "bargain_user":self.bargain_user.natural_key(),
                "bargain_friend":self.bargain_friend.natural_key(),
                "rank":self.rank}
