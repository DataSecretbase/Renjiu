from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
import django.utils.timezone as timezone
from django.dispatch import receiver
from django.core import validators
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
import random
import time
from uuid import uuid4
from datetime import datetime, date

from .datasettings import league_model as m_set
# Create your models here.


class DriverSchool(models.Model):
    province_id = models.IntegerField(verbose_name='省', default=0)
    city_id = models.IntegerField(verbose_name='城市', default=0)
    district_id = models.IntegerField(verbose_name='区', default=0)
    name = models.CharField(verbose_name='店铺名称', max_length=30)
    address = models.CharField(verbose_name='地址', max_length=100, blank=True, null=True)
    phone = models.CharField(verbose_name='联系电话', max_length=50, blank=True, null=True)
    introduce = models.TextField(verbose_name='驾校介绍')
    characteristic = models.TextField(verbose_name='驾校特色')
    sort = models.IntegerField(verbose_name='排序')
    pic = models.ForeignKey('Icon', verbose_name='驾校商标', on_delete=models.DO_NOTHING)
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


class BookSet(models.Model):
    coach_driver_school = models.ForeignKey('CoachDriverSchool', on_delete=models.CASCADE, verbose_name='教练所属驾校')
    num_student = models.SmallIntegerField(verbose_name="预约学生数量")
    book_date_start = models.DateTimeField(verbose_name="预约设置开始的日期", null=True)
    book_date_end = models.DateTimeField(verbose_name="预约设置结束的日期", null=True)
    cur_book = models.SmallIntegerField(verbose_name="当前已经预约学生", default=0)
    status = models.SmallIntegerField(verbose_name="预约状态", default=0)
    set_type = models.SmallIntegerField(verbose_name='设置类型', default=0, choices=m_set.BOOK_SET_TYPE)

    class Meta:
        db_table = 'BookSet'
        verbose_name = '预约设置'
        verbose_name_plural = "预约设置"

    def __str__(self):
        return self.coach_driver_school.coach.name + \
               " "+self.coach_driver_school.train_ground.name

    def natural_key(self):
        return {"id": self.id,
                "coach_driver_school": self.coach_driver_school.natural_key(),
                "num_student": self.num_student,
                "book_datetime": self.book_datetime,
                "cur_book": self.cur_book,
                "status": self.status,
                "set_type": self.get_set_type_display()}


class CoachDriverSchool(models.Model):
    coach = models.ForeignKey('WechatUser', on_delete=models.SET_NULL, verbose_name="教练", null=True, blank=True)
    train_ground = models.ForeignKey('DriverSchool', on_delete=models.DO_NOTHING, verbose_name="训练场id")

    class Meta:
        db_table = "CoachDriverSchool"
        verbose_name = "教练所属驾校"
        verbose_name_plural = "教练所属驾校"
    
    def __str__(self):
        return self.coach.name + " " + self.train_ground.name

    def natural_key(self):
        return {"id": self.id,
                "coach": self.coach.natural_key(),
                "train_ground": self.train_ground.natural_key()}


class UserExam(models.Model):
    user_id = models.ForeignKey('WechatUser', verbose_name="考生", on_delete=models.CASCADE)
    exam_status = models.SmallIntegerField(verbose_name="考试状态", choices=m_set.EXAM_STATUS)
    exam_type = models.SmallIntegerField(verbose_name="考试类型", choices=m_set.EXAM_TYPE)
    exam_results = models.FloatField(verbose_name="考试成绩")
    train_ground = models.ForeignKey('DriverSchool', on_delete=models.DO_NOTHING, verbose_name="训练场id")
    date_add = models.DateTimeField(verbose_name="考试开始时间", auto_now_add=True)
    date_end = models.DateTimeField(verbose_name="考试结束时间", auto_now=True)

    class Meta:
        db_table = 'UserExam'
        verbose_name = '学生考试信息'
        verbose_name_plural = '学生考试信息'
    
    def __str__(self):
        return self.user_id.name + " " + self.get_exam_type_display()

    def natural_key(self):
        return {"id": self.id,
                "user_id": self.user_id.natural_key(),
                "exam_status": self.exam_status,
                "exam_type": self.exam_type,
                "exam_results": self.exam_results,
                "date_add": self.date_add,
                "date_and": self.date_end}


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """
    Generate a token every time a new account object
    is created.
    """
    if created:
        Token.objects.create(user=instance)


class AccountManager(BaseUserManager):
    def _create_user(self, email, username, password, avatar,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a Account with the given email, username and password.
        """
        now = timezone.now()

        if not email:
            raise ValueError('Users must have a valid email address.')

        if not username:
            raise ValueError('The given username must be set')

        email = self.normalize_email(email)
        try:
            del extra_fields['confirm_password']
        except KeyError:
            pass

        account = self.model(email=email, username=username, avatar=avatar,
                             is_staff=is_staff, is_active=True,
                             is_superuser=is_superuser, last_login=now,
                             date_joined=now, **extra_fields)

        account.set_password(password)
        account.save(using=self._db)
        return account

    def create_user(self, username, password, avatar=None, email=None, **extra_fields):
        return self._create_user(email, username, password, avatar, False, False,
                                 **extra_fields)

    def create_superuser(self, email, username, password, avatar=None, **extra_fields):
        return self._create_user(email, username, password, avatar, True, True, **extra_fields)


class WechatUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name=_('email address'),
        max_length=255,
        unique=True,
    )
    username = models.CharField(_('username'), max_length=30, blank=True,
                                help_text=_('Required. 30 characters or fewer. Letters, digits'
                                            ' and ./+/-/_ only.'),
                                validators=[
                                    validators.RegexValidator(r'^[\w.+-]+$',
                                                              _('Enter a valid username jebal.'),
                                                              'invalid')
                                ])
    cookie = models.CharField(verbose_name='用户认证标识', max_length=100, default='', blank=True)
    name = models.CharField(verbose_name='昵称', max_length=40, blank=True)
    openid = models.CharField(verbose_name='OpenId', max_length=255, blank=True)
    union_id = models.CharField(verbose_name='UnionId', max_length=255, blank=True)
    language = models.CharField(verbose_name='语言', max_length=40, blank=True)
    user_type = models.SmallIntegerField(verbose_name='用户类型', choices=m_set.USER_TYPE, default=0)
    register_type = models.SmallIntegerField(verbose_name='注册来源', default=0)
    phone = models.CharField(verbose_name='手机号码', max_length=50, blank=True)
    country = models.IntegerField(verbose_name='国家', default=0, blank=True)
    province = models.IntegerField(verbose_name='省份', default=0)
    city = models.IntegerField(verbose_name='城市', default=0)
    avatar = models.ForeignKey('Icon', verbose_name='头像', on_delete=models.SET_DEFAULT,
                               default=0, null=True, blank=True)
    register_ip = models.CharField(verbose_name='注册IP', max_length=80, blank=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    ip = models.CharField(verbose_name='登陆IP', max_length=80, blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'WechatUser'
        verbose_name = '微信用户'
        verbose_name_plural = '微信用户'
        swappable = 'AUTH_USER_MODEL'

    def natural_key(self):
        return {"url": "https://qgdxsw.com:8000"+self.avatar.display_pic.url,
                "name": self.name,
                "id": self.id}

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def get_address(self):
        return self.country

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Goods(models.Model):
    category_id = models.ForeignKey('Category', on_delete=models.SET_DEFAULT, default=0)
    characteristic = models.CharField(verbose_name="描述", max_length=100, default='')
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
    pic = models.ForeignKey('Icon', verbose_name="商品图片连接",
                            on_delete=models.SET_DEFAULT, default=0)
    pingtuan = models.BooleanField(verbose_name="拼团", default=False)
    recommend_status = models.SmallIntegerField(verbose_name="推荐状态", default=0)
    shop_id = models.ForeignKey("DriverSchool", verbose_name="商店id", on_delete=models.CASCADE)
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
    wechat_user_id = models.ForeignKey('WechatUser', verbose_name='微信用户', on_delete=models.DO_NOTHING)
    number_goods = models.IntegerField(verbose_name='商品数量', default=0)
    goods_price = models.FloatField(verbose_name='商品总金额', default=0)
    coupons_id = models.IntegerField(verbose_name='使用的优惠券id', default=0)
    total = models.FloatField('实际支付', default=0)
    ORDER_STATUS = [(0, "待付款"), (1, '待发货'),
                    (2, '待收货'), (3, '待评价'),
                    (4, '已完成'), (5, '已删除')]
    status = models.SmallIntegerField(verbose_name='状态', choices=ORDER_STATUS, default=0)
    remark = models.CharField(verbose_name='备注', max_length=100, blank=True)
    linkman = models.CharField(verbose_name='联系人', max_length=100, blank=True)
    phone = models.CharField(verbose_name='手机号码', max_length=50, blank=True)
    province_id = models.SmallIntegerField(verbose_name='省', default=0)
    city_id = models.SmallIntegerField(verbose_name='市', default=0)
    district_id = models.SmallIntegerField(verbose_name='区', default=0)
    address = models.CharField(verbose_name='详细地址', max_length=100, blank=True)
    postcode = models.CharField(verbose_name='邮政编码', max_length=20, blank=True)
    date_add = models.DateTimeField(verbose_name='下单时间', auto_now_add=True)

    class Meta:
        db_table = 'Order'
        verbose_name = '订单'
        verbose_name_plural = '订单'

    def __str__(self):
        return "{0}".format(self.id)


class OrderGoods(models.Model):
    order_id = models.IntegerField(verbose_name='订单', default=0)
    # 冗余记录商品，防止商品删除后订单数据不完整
    goods_id = models.IntegerField(verbose_name='商品id', default=0)
    name = models.CharField(verbose_name='商品名称', max_length=50, blank=True)
    display_pic = models.ForeignKey('Icon', verbose_name='图片',
                                    on_delete=models.SET_DEFAULT, default=0)
    property_str = models.CharField(verbose_name='商品规格', max_length=200, blank=True)
    price = models.FloatField(verbose_name='单价', default=0)
    amount = models.IntegerField(verbose_name='商品数量', default=0)
    total = models.FloatField(verbose_name='总价', default=0)
    
    class Meta:
        db_table = 'OrderGoods'
        verbose_name = '订单商品'
        verbose_name_plural = '订单商品'

    def __str__(self):
        return self.name


class ModifyPriceWizard(models.Model):
    order_id = models.ForeignKey('Order', verbose_name='订单', on_delete=models.CASCADE)
    total = models.FloatField(verbose_name='金额')

    class Meta:
        db_table = 'ModifyPriceWizard'
        verbose_name = '修改价格'
        verbose_name_plural = '修改价格'

    def natural_key(self):
        return {"id": self.id,
                "order_id": self.order_id,
                "total": self.total}


class DeliverWizard(models.Model):
    _name = 'wechat_mall.deliver.wizard'
    order_id = models.ForeignKey('Order', verbose_name='订单', on_delete=models.CASCADE)
    shipper_id = models.ForeignKey('Shipper', verbose_name='快递承运商', on_delete=models.CASCADE)
    tracking_number = models.CharField(verbose_name='运单号', max_length=200)
    status = models.CharField(verbose_name='状态', max_length=20)

    class Meta:
        db_table = 'DeliverWizard'
        _description = '发货'

    def natural_key(self):
        return {"id": self.id,
                "order_id": self.order_id,
                "shipper_id": self.shipper_id,
                "tracking_number": self.tracking_number,
                "status": self.status}


class Shipper(models.Model):
    name = models.CharField(verbose_name='名称', max_length=50)
    code = models.CharField(verbose_name='编码', max_length=100)

    class Meta:
        db_table = 'Shipper'
        verbose_name = '承运商'
        verbose_name_plural = '承运商'

    def __str__(self):
        return self.name

    def natural_key(self):
        return {"id": self.id,
                "name": self.name,
                "code": self.code}


class Logistics(models.Model):
    name = models.CharField('名称', max_length=50)
    by_self = models.BooleanField(verbose_name='商家配送', default=False)
    free = models.BooleanField(verbose_name='是否包邮', default=False)
    valuation_type = models.SmallIntegerField(verbose_name='计价方式', default=0)

    class Meta:
        db_table = 'Logistics'
        verbose_name = '物流信息'
        verbose_name_plural = '物流信息'
    
    def __str__(self):
        return self.name

    def natural_key(self):
        return {"id": self.id,
                "name": self.name,
                "by_self": self.name,
                "free": self.free,
                "valuation_type": self.valuation_type}


class Category(models.Model):
    name = models.CharField(verbose_name='名称', max_length=100)
    eng_name = models.CharField(verbose_name='名称(英文)', max_length=100)
    category_type = models.CharField(verbose_name='类型', max_length=30)
    pid = models.ForeignKey('Category', verbose_name='上级分类',
                            on_delete=models.SET_DEFAULT, default=0)
    key = models.IntegerField(verbose_name='编号')
    icon = models.ForeignKey('Icon', verbose_name='图标', on_delete=models.CASCADE)
    level = models.SmallIntegerField(verbose_name='分类级别')
    is_use = models.BooleanField(verbose_name='是否启用', default=True)
    sort = models.IntegerField(verbose_name='排序')
    
    class Meta:
        db_table = 'Category'
        verbose_name = '商品分类'
        verbose_name_plural = '商品分类'
        _order = 'level,sort'

    def __str__(self):
        return self.name


def filepath(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid4().hex, ext)
    year = datetime.now().year
    month = datetime.now().month
    day = datetime.now().day
    return "img/{0}/{1}/{2}/{3}".format(year, month, day, filename)


class Icon(models.Model):
    name = models.CharField(verbose_name="图标名称", max_length=20)
    display_pic = models.ImageField(verbose_name="icon 对应", upload_to=filepath)
    
    class Meta:
        db_table = 'Icon'
        verbose_name = '图标'
        verbose_name_plural = '图标'

    def __str__(self):
        return self.name


class Attachment(models.Model):
    
    display_pic = models.ImageField(verbose_name="附件图片", upload_to=filepath)
    owner_id = models.ForeignKey("Goods", verbose_name="所属货物",
                                 on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'Attachment'
        verbose_name = '图片'
        verbose_name_plural = '图片'

    def __str__(self):
        return self.owner_id.name


class Payment(models.Model):

    order_id = models.ForeignKey('Order', verbose_name='订单', on_delete=models.CASCADE)
    payment_number = models.CharField(verbose_name='支付单号', max_length=255)
    wechat_user_id = models.ForeignKey('WechatUser', verbose_name='微信用户',
                                       on_delete=models.DO_NOTHING)
    price = models.FloatField(verbose_name='支付金额(元)')
    status = models.SmallIntegerField(verbose_name='状态', choices=m_set.PAYMENT_STATUS, default=1)
    openid = models.CharField(verbose_name='openid', max_length=255)
    result_code = models.CharField(verbose_name='业务结果', max_length=30)
    err_code = models.CharField(verbose_name='错误代码', max_length=40)
    err_code_des = models.CharField(verbose_name='错误代码描述', max_length=255)
    transaction_id = models.CharField(verbose_name='微信订单号', max_length=255)
    bank_type = models.CharField(verbose_name='付款银行', max_length=50)
    fee_type = models.CharField(verbose_name='货币种类', max_length=20)
    total_fee = models.FloatField(verbose_name='订单金额(分)')
    settlement_total_fee = models.FloatField(verbose_name='应结订单金额(分)')
    cash_fee = models.FloatField(verbose_name='现金支付金额')
    cash_fee_type = models.CharField(verbose_name='现金支付货币类型', max_length=40)
    coupon_fee = models.FloatField(verbose_name='代金券金额(分)')
    coupon_count = models.IntegerField(verbose_name='代金券使用数量')

    class Meta:
        db_table = 'Payment'
        verbose_name = '支付记录'
        verbose_name_plural = '支付记录'

    def __str__(self):
        return self.id


class Address(models.Model):
    province_id = models.IntegerField(verbose_name='省', default=0)
    city_id = models.IntegerField(verbose_name='城市', default=0)
    district_id = models.IntegerField(verbose_name='区', default=0)
    link_man = models.CharField(verbose_name='联系人', max_length=15)
    address = models.CharField(verbose_name='详细地址', max_length=100)
    mobile = models.CharField(verbose_name='电话号码', max_length=40)
    code = models.CharField(verbose_name='邮政编码', max_length=20)
    is_default = models.BooleanField(verbose_name='默认地址', default=False)
    owner_type = models.SmallIntegerField(verbose_name="被标注地址的类型eg:微信用户,订单")
    owner_id = models.IntegerField(verbose_name="微信用户、订单的id")

    class Meta:
        db_table = 'Address'
        verbose_name = '地址'
        verbose_name_plural = '地址'

    def natural_key(self):
        return {"id": self.id,
                "province_id": self.province_id,
                "city_id": self.city_id,
                "district_id": self.district_id,
                "link_man": self.link_man,
                "address": self.address,
                "mobile": self.mobile,
                "code": self.code,
                "is_default": self.is_default,
                "owner_type": self.owner_type,
                "owner_id": self.owner_id}


class Coupons(models.Model):
    name = models.CharField(verbose_name='优惠券名称', max_length=50)
    money_min = models.FloatField(verbose_name='优惠券金额')
    money_hreshold = models.FloatField(verbose_name='满 减 最低额度')
    DATE_END_TYPE = ((0, "截止某日前有效"), (1, "领取后有效时间倒计"))
    date_end_type = models.SmallIntegerField(verbose_name='优惠券有效期类型', choices=DATE_END_TYPE)
    date_end_days = models.DateTimeField(verbose_name="优惠券截止时间", default=timezone.now)
    goods_id = models.ForeignKey('Goods', on_delete=models.CASCADE, verbose_name="商品id")
    is_active = models.BooleanField(verbose_name="优惠券是否有效")
    date_add = models.DateTimeField(verbose_name="优惠券添加的时间", default=timezone.now)
    coupons_type = models.SmallIntegerField(verbose_name="优惠券类型1.通用型,2.分类专用型,3.商品专用型,4.店铺专用型", default=0)

    class Meta:
        db_table = 'Coupons'
        verbose_name = "优惠券"
        verbose_name_plural = "优惠券"

    def __str__(self):
        return self.name

    def natural_key(self):
        return {"id": self.id,
                "name": self.name,
                "money_min": self.money_min,
                "money_hreshold": self.money_hreshold,
                "is_active": self.is_active,
                "date_add": self.date_add,
                "coupons_type": self.coupons_type}


class Coupons_users(models.Model):
    coupons_id = models.ForeignKey('Coupons', on_delete=models.CASCADE, verbose_name="优惠券id")
    user_id = models.ForeignKey('WechatUser', on_delete=models.CASCADE, verbose_name="用户id")
    date_add = models.DateTimeField(verbose_name="优惠券添加的时间", default=timezone.now)
    date_end_days = models.DateTimeField(verbose_name="优惠券截止时间", default=timezone.now)

    class Meta:
        db_table = 'Coupons_users'
        verbose_name = "用户领取的优惠券"
        verbose_name_plural = "用户领取的优惠券"

    def __str__(self):
        return self.coupons_id.name+self.user_id.name

    def natural_key(self):
        return {"id": self.id,
                "coupons_id": self.coupons_id,
                "user_id": self.user_id,
                "date_add": self.date_add,
                "date_end_days": self.date_end_days}


class Book(models.Model):
    coach = models.ForeignKey('WechatUser', related_name='coach_wechatuser',
                              on_delete=models.CASCADE, verbose_name="教练")
    user = models.ForeignKey('WechatUser', related_name='user_wechatuser',
                             on_delete=models.DO_NOTHING, verbose_name='学员')
    train_ground = models.ForeignKey('DriverSchool', on_delete=models.CASCADE, verbose_name="训练场id")
    book_time_start = models.DateTimeField(verbose_name="预约开始时间")
    book_time_end = models.DateTimeField(verbose_name="预约结束时间")
    last_active_time = models.DateTimeField('最近操作时间', auto_now=True)
    status = models.SmallIntegerField(verbose_name='预约状态', default=0)
    
    class Meta:
        db_table = 'Book'
        verbose_name = '学员教练预约'
        verbose_name_plural = "学员教练预约"

    def __str__(self):
        return "教练"
    

class Bargain(models.Model):
    goods_id = models.ForeignKey('Goods', on_delete=models.CASCADE, verbose_name='货物')
    times = models.IntegerField(verbose_name='砍价次数', default=0)
    price = models.FloatField(verbose_name='砍价当前价格')
    min_price = models.FloatField(verbose_name='砍价最低价格')
    calculate_method = models.SmallIntegerField(verbose_name='砍价计算模式', choices=m_set.BARGAIN_CALCULATE_METHOD)
    expected_price = models.FloatField(verbose_name='期望砍价价格')
    expected_times = models.FloatField(verbose_name='期望砍价次数')
    date_start = models.DateTimeField(verbose_name='活动开始时间', auto_now_add=True)
    date_end = models.DateTimeField(verbose_name='活动结束时间')

    class Meta:
        db_table = 'Bargain'
        verbose_name = '砍价'
        verbose_name_plural = '砍价'

    def __str__(self):
        return self.goods_id.name

    def natural_key(self):
        return {"id": self.id,
                "goods": self.goods_id.natural_key(),
                "times": self.times,
                "price": self.price,
                "min_price": self.min_price,
                "expected_price": self.expected_price,
                "expected_times": self.expected_times,
                "date_start": self.date_start,
                "date_end": self.date_end}


class BargainUser(models.Model):
    bargain_id = models.ForeignKey('Bargain', on_delete=models.CASCADE, verbose_name='砍价活动')
    user_id = models.ForeignKey('WechatUser', on_delete=models.CASCADE, verbose_name='砍价用户')
    bargain_date = models.DateTimeField(verbose_name="砍价发起时间", auto_now_add=True)

    class Meta:
        db_table = 'BargainUser'
        verbose_name = '砍价用户记录'
        verbose_name_plural = '砍价用户记录'

    def __str__(self):
        return self.bargain_id.goods_id.name+self.user_id.name

    def natural_key(self):
        return {"id": self.id,
                "bargain_id": self.bargain_id.natural_key(),
                "user_id": self.user_id.natural_key()}


class BargainFriend(models.Model):
    bargain_user_id = models.ForeignKey('BargainUser', on_delete=models.CASCADE, verbose_name='砍价发起用户')
    bargain_friend_id = models.ForeignKey('WechatUser', on_delete=models.CASCADE, verbose_name='参与砍价好友')
    rank = models.IntegerField(verbose_name="砍价次序")
    date_add = models.DateTimeField(verbose_name='砍价时间', auto_now_add=True)

    class Meta:
        db_table = 'BargainFriend'
        verbose_name = '帮忙砍价的好友'
        verbose_name_plural = "帮忙砍价的好友"

    def __str__(self):
        return self.bargain_user_id.user_id.name+self.bargain_friend_id.name
 
    def natural_key(self):
        return {"id": elf.id,
                "bargain_user_id": self.bargain_user_id.natural_key(),
                "bargain_friend_id": self.bargain_friend_id.natural_key(),
                "rank": self.rank}


class GoodsReputation(models.Model):
    goods_id = models.ForeignKey('Goods', on_delete=models.CASCADE, verbose_name='商品')
    user_id = models.ForeignKey('WechatUser', on_delete=models.DO_NOTHING, verbose_name='评论用户')
    goods_reputation_str = models.CharField(verbose_name="评价级别", max_length=20)
    goods_reputation_remark = models.TextField(verbose_name="评论备注")
    dates_reputation = models.DateTimeField(verbose_name="评论日期", auto_now_add=True)

    class Meta:
        db_table = 'GoodsReputation'
        verbose_name = '商品评论'
        verbose_name_plural = '商品评论'
    
    def __str__(self):
        return self.goods_id.name

    def natural_key(self):
        return {"id": self.id,
                "goods_id": self.user_id,
                "goods_reputation_str": self.goods_reputation_str,
                "goods_reputation_remark": self.goods_reputation_remark,
                "dates_reputation": self.dates_reputation}


''''
forum 论坛 社区 交流
社区 主题 表
'''


class Forum(models.Model):
    user_id = models.ForeignKey('WechatUser', on_delete=models.DO_NOTHING, verbose_name='帖子发表者')
    title = models.CharField(max_length=50, verbose_name='标题')
    content = models.TextField(verbose_name='帖子内容')
    Topic_id = models.ForeignKey('Topic', on_delete=models.DO_NOTHING, verbose_name='主题')
    repley_count = models.IntegerField(verbose_name='回复数量', default=0)
    time_add = models.DateTimeField(verbose_name='添加时间', auto_now_add=True)
    last_reply_time = models.DateTimeField(verbose_name='最后回复时间', auto_now=True)

    class Meta:
        db_table = 'Forum'
        verbose_name = '帖子'
        verbose_name_plural = '帖子'

    def __str__(self):
        return self.user_id.name + self.title


class Topic(models.Model):
    name = models.CharField(max_length=30, verbose_name='主题名字')
    description = models.CharField(max_length=255, verbose_name='主题介绍')
    eng_name = models.CharField(verbose_name='名称(英文)', max_length=100)
    pid = models.ForeignKey('Category', verbose_name='上级主题',
                            on_delete=models.SET_DEFAULT, default=0)
    icon = models.ForeignKey('Icon', verbose_name='图标', on_delete=models.CASCADE)
    level = models.SmallIntegerField(verbose_name='分类级别')
    is_use = models.BooleanField(verbose_name='是否启用', default=True)
    sort = models.IntegerField(verbose_name='排序')

    class Meta:
        db_table = 'Topic'
        verbose_name = '主题'
        verbose_name_plural = '主题'

    def __str__(self):
        return self.name

    def natural_key(self):
        return {'id': self.id,
                'name': self.name,
                'description': self.description,
                'eng_name': self.eng_name,
                'pid': self.pid,
                'icon': self.icon,
                'level': self.level,
                'is_use': self.is_use,
                'sort': self.sort}

 
class ForumReply(models.Model):
    forum_id = models.ForeignKey('Forum', on_delete=models.CASCADE, verbose_name='论坛内容')
    user_id = models.ForeignKey('WechatUser', on_delete=models.SET_DEFAULT,
                                default='用户已注销', verbose_name='回复用户')
    content = models.TextField(verbose_name='回复内容')

    class Meta:
        db_table = 'ForumReply'
        verbose_name = '帖子回复'
        verbose_name_plural = '帖子回复'

    def __str__(self):
        return self.user_id.name+self.content


class ViewedProfileTracking(models.Model):
    actor = models.ForeignKey(WechatUser, related_name='who_visit_profile', on_delete=models.SET_NULL, null=True, blank=True)
    visited_profile = models.ForeignKey(WechatUser, related_name='visited_profile', on_delete=models.SET_NULL, null=True, blank=True)
    visited_time = models.DateTimeField(auto_now_add=True)