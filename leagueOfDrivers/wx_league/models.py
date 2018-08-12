from django.db import models
from django.contrib.auth.models import AbstractUser
import django.utils.timezone as timezone
import random
import time
from uuid import uuid4
from datetime import datetime
# Create your models here.

class DriverSchool(models.Model):

	#shop_type = fields.Char('店铺类型')

    province_id = models.IntegerField(verbose_name = '省', default = 0)
    #PROVINCE = ((0,'beijin'),)
    #CITY = ((0,'beijin'),(1,"shanghai"))
    city_id = models.IntegerField(verbose_name = '城市', default = 0)
    #DISTRICT = ((0,'beijin'))
    district_id = models.IntegerField(verbose_name = '区', default = 0)
    name = models.CharField(verbose_name = '店铺名称', max_length = 30)
    address = models.CharField(verbose_name='地址', max_length=100,blank = True, null = True)
    phone = models.CharField(verbose_name = '联系电话', max_length=50, blank = True, null = True)
    introduce = models.TextField(verbose_name='驾校介绍')
    characteristic = models.TextField(verbose_name = '驾校特色')
    sort = models.IntegerField(verbose_name = '排序')
    pic = models.ForeignKey('Icon', verbose_name='驾校商标', on_delete = models.DO_NOTHING)
    activity = models.CharField(verbose_name = '打折优惠信息', max_length=255)
    latitude = models.FloatField(verbose_name = '纬度')
    longitude = models.FloatField(verbose_name = '经度')
    number_good_reputation = models.IntegerField(verbose_name = '好评数')
    number_order = models.IntegerField(verbose_name = '订单数')

    class Meta:
        db_table = 'DriverSchool'
        _description = '驾校'
        _order = 'sort'
	

class WechatUser(AbstractUser):
 
    cookie = models.CharField('用户认证标识', max_length=100,default='', blank = True)
    name = models.CharField(verbose_name = '昵称', max_length = 40, blank = True)
    openid = models.CharField(verbose_name = 'OpenId', max_length = 255, blank = True)
    union_id = models.CharField(verbose_name = 'UnionId', max_length = 255, blank = True)
    gender = models.SmallIntegerField(verbose_name = 'gender',default = 0, blank = True)
    language = models.CharField(verbose_name = '语言', max_length = 40, blank = True)
    #REGISTERTYPE = ((0,"beijin"))
    register_type = models.SmallIntegerField( verbose_name='注册来源',
                                     default=0)
    phone = models.CharField(verbose_name = '手机号码', max_length = 50, blank = True)
    #COUNTRY = ((0,"beijin"))
    country = models.IntegerField(verbose_name = '国家', default = 0, blank = True) 
    #PROVINCE = ((0,"beijin"))
    province = models.IntegerField(verbose_name = '省份', default = 0)
    #CITY = ((0,"beijin"))
    city = models.IntegerField(verbose_name = '城市', default = 0)
    avatar = models.ImageField(verbose_name = '头像', upload_to='upload', blank = True)
    register_ip = models.CharField(verbose_name = '注册IP', max_length = 80, blank = True)
    #last_login = models.DateTimeField(verbose_name = '登陆时间')
    ip = models.CharField(verbose_name = '登陆IP', max_length = 80, blank = True)
    
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'WechatUser'
        _description = '微信用户'


    #address_ids = fields.One2many('wechat_mall.address', 'wechat_user_id', string='收货地址')
    #order_ids = fields.One2many('wechat_mall.order', 'wechat_user_id', string='订单')

class goods(models.Model):
    barCode = models.CharField('条形码', max_length = 100, default = '')
    category_id = models.ForeignKey('Category', on_delete = models.SET_DEFAULT, default = 0)
    characteristic = models.CharField(verbose_name = "描述", max_length = 100, default = '')
    commission = models.FloatField(verbose_name = "佣金")
    commission_type = models.IntegerField(verbose_name = "佣金类型", default = 0)
    dateAdd = models.DateTimeField(verbose_name = '上架时间', auto_now_add = True)
    dateStart = models.DateTimeField(verbose_name = '上架时间', auto_now_add = True)
    dateUpdate = models.DateTimeField(verbose_name = '更新时间', auto_now = True)
    logistics_id = models.IntegerField(verbose_name = '物流id', default = 0)
    minPrice = models.FloatField(verbose_name = '最小价格',)
    minScore = models.SmallIntegerField(verbose_name = '最小评分', default = 0)
    name = models.CharField(verbose_name = '名称', max_length = 60)
    numberFav = models.IntegerField(default = 0)
    numberGoodReputation = models.IntegerField(default = 0)
    numberOrders = models.IntegerField(verbose_name = '已售数量',default = 0)
    originalPrice = models.FloatField(verbose_name = "原价")
    paixu = models.IntegerField(default = 0)
    pic = models.ForeignKey('Icon', verbose_name = "商品图片连接", on_delete = models.SET_DEFAULT, default = 0)
    pingtuan = models.BooleanField(verbose_name = "拼团" , default = False)
    pingtuanPrice = models.FloatField(verbose_name = "拼团价格", default = 0.00)
    recommendStatus = models.SmallIntegerField(verbose_name = "推荐状态", default = 0)
    recommendStatusStr = models.CharField(verbose_name ="推荐状态(文字)", max_length = 10)
    shop_id = models.ForeignKey("DriverSchool",verbose_name = "商店id", on_delete = models.CASCADE)
    status = models.SmallIntegerField(verbose_name  = "商品状态", default = 0)
    statusStr = models.CharField(verbose_name ="商品状态(文字)", max_length = 10)
    stores = models.IntegerField(verbose_name = "库存")
    user_id = models.IntegerField(default = 0)
    video_id = models.IntegerField(default = 0)
    views = models.IntegerField(default = 0)
    weight = models.FloatField(default = 0.00)
    


class Order(models.Model):
    wechat_user_id = models.ForeignKey('WechatUser', verbose_name ='微信用户', on_delete = models.DO_NOTHING)
    #goods_ids= models.ManyToManyField('Goods', verbose_name='商品真实数据冗余')
    #order_goods_ids = fields.One2many('wechat_mall.order.goods', 'order_id',
                                      #verbose_name='订单商品', help='商品参数数据冗余，防止商品修改或删除。')
    number_goods = models.IntegerField(verbose_name = '商品数量',default = 0)
    goods_price = models.FloatField(verbose_name = '商品总金额', default=0)
    logistics_price = models.FloatField(verbose_name = '物流费用', default=0)
    total = models.FloatField('实际支付', default=0 )
    ORDER_STATUS = [(0,"待付款"),(1,'待发货'),(2,'待收货'),(3,'待评价'),(4,'已完成'),(5,'已删除')]
    status = models.SmallIntegerField(verbose_name = '状态', choices = ORDER_STATUS, default = 0)
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

    shipper_id = models.ForeignKey('Shipper', verbose_name='快递承运商', on_delete = models.DO_NOTHING, default = 1)
    tracking_number = models.CharField(verbose_name = '运单号', max_length = 200, blank = True)
    #display_traces = fields.Html('物流信息', compute='_compute_display_traces')
    traces = models.TextField(verbose_name = '物流信息', blank = True)

    dateAdd = models.DateTimeField(verbose_name = '下单时间', default = timezone.now)
    class Meta:
        db_table = "Order"
        _inherit = ['mail.thread']
        _rec_name = 'order_num'
        _order = 'create_date desc'
        _description = '订单'
    #payment_ids = fields.One2many('wechat_mall.payment', 'order_id', '支付记录')

class OrderGoods(models.Model):
    order_id = models.IntegerField(verbose_name='订单', default = 0)

    # 冗余记录商品，防止商品删除后订单数据不完整
    goods_id = models.IntegerField(verbose_name = '商品id',default = 0)
    name = models.CharField(verbose_name = '商品名称', max_length = 50, blank =True)
    display_pic = models.ImageField(verbose_name = '图片', blank = True)
    property_str = models.CharField(verbose_name = '商品规格', max_length = 200, blank = True)
    price = models.FloatField(verbose_name = '单价', default = 0)
    amount = models.IntegerField(verbose_name = '商品数量', default = 0)
    total = models.FloatField(verbose_name = '总价', default = 0)
    
    class Meta:
        db_table = 'OrderGoods'
        _description = '订单商品'


class ModifyPriceWizard(models.Model):
    _name = 'wechat_mall.modify.price.wizard'
    _description = '修改价格'

    order_id = models.ForeignKey('Order', verbose_name ='订单', on_delete = models.CASCADE)
    total = models.FloatField(verbose_name = '金额')
    class Meta:
        db_table = 'ModifyPriceWizard'


class DeliverWizard(models.Model):
    _name = 'wechat_mall.deliver.wizard'

    order_id = models.ForeignKey('Order', verbose_name='订单', on_delete = models.CASCADE)
    shipper_id = models.ForeignKey('Shipper', verbose_name='快递承运商', on_delete = models.CASCADE)
    tracking_number = models.CharField(verbose_name = '运单号', max_length = 200)
    status = models.CharField(verbose_name = '状态', max_length = 20)
    class Meta:
        db_table = 'DeliverWizard'
        _description = '发货'


class Shipper(models.Model):
    name =  models.CharField(verbose_name = '名称', max_length = 50)
    code = models.CharField(verbose_name = '编码', max_length = 100)

    class Meta:
        db_table = 'Shipper'
        _description = '承运商'


class Logistics(models.Model):
    name = models.CharField('名称', max_length = 50)
    by_self = models.BooleanField(verbose_name = '商家配送', default = False)
    free = models.BooleanField(verbose_name = '是否包邮', default = False)
    #LogisticsValuationType = ((0,"22"))
    valuation_type = models.SmallIntegerField(verbose_name='计价方式'
                                      ,default=0)

    class Meta:
        db_table = 'Logistics'
        _description = '物流'
    #transportation_ids = fields.One2many('wechat_mall.transportation', 'logistics_id', string='运送费用')
    #district_transportation_ids = fields.One2many('wechat_mall.district.transportation', 'logistics_id',
                                                  #string='区域运送费用')



class Category(models.Model):
    name = models.CharField(verbose_name='名称', max_length = 100)
    category_type = models.CharField(verbose_name = '类型',max_length = 30)
    pid = models.ForeignKey('Category', verbose_name='上级分类', on_delete = models.SET_DEFAULT, default = 0)
    key = models.IntegerField(verbose_name='编号')
    icon = models.ForeignKey('Icon', verbose_name='图标', on_delete = models.CASCADE)
    level = models.SmallIntegerField(verbose_name='分类级别')
    is_use = models.BooleanField(verbose_name='是否启用', default=True)
    sort = models.IntegerField(verbose_name='排序')
    
    class Meta:
        db_table = 'Category'
        _description = '商品分类'
        _order = 'level,sort'

   #goods_ids = fields.One2many('wechat_mall.goods', 'category_id', '商品')

def filepath(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid4().hex, ext)
    year = datetime.now().year
    month =datetime.now().month
    day = datetime.now().day
    return "img/{0}/{1}/{2}/{3}".format(year,month,day,filename)

class Icon(models.Model):
    display_pic = models.ImageField(verbose_name = "icon 对应",upload_to=filepath)
    
    class Meta:
        db_table = 'Icon'


class Attachment(models.Model):
    OWNER_TYPE = (("DriverSchool","DriverSchool"),("WechatUser","WechatUser"),("Goods","Goods"),("Unkown","Unkown"))
    
    display_pic = models.ImageField(verbose_name = "附件图片",upload_to='img')
    owner_id = models.IntegerField(default = 0)
    owner_type = models.CharField(choices = OWNER_TYPE, max_length = 20, default = "Unkown")
    
    class Meta:
        db_table = 'Attachment'



class Payment(models.Model):

    order_id = models.ForeignKey('Order', verbose_name = '订单', on_delete = models.CASCADE)
    payment_number = models.CharField(verbose_name = '支付单号', max_length = 255)
    wechat_user_id = models.ForeignKey('WechatUser', verbose_name = '微信用户', on_delete = models.DO_NOTHING)
    price = models.FloatField(verbose_name = '支付金额(元)')
    #PAYMENT_STATUS = ((0,"22"))
    status = models.SmallIntegerField(verbose_name = '状态', default=0)
    # 微信notify返回参数
    openid = models.CharField(verbose_name = 'openid', max_length = 255)
    result_code = models.CharField(verbose_name = '业务结果', max_length = 30)
    err_code = models.CharField(verbose_name = '错误代码', max_length = 40)
    err_code_des = models.CharField(verbose_name = '错误代码描述', max_length = 255)
    transaction_id = models.CharField(verbose_name = '微信订单号', max_length = 255)
    bank_type = models.CharField(verbose_name = '付款银行', max_length = 50)
    fee_type = models.CharField(verbose_name = '货币种类', max_length = 20)
    total_fee = models.FloatField(verbose_name = '订单金额(分)')
    settlement_total_fee = models.FloatField(verbose_name = '应结订单金额(分)')
    cash_fee = models.FloatField(verbose_name = '现金支付金额')
    cash_fee_type = models.CharField(verbose_name = '现金支付货币类型', max_length = 40)
    coupon_fee = models.FloatField(verbose_name = '代金券金额(分)')
    coupon_count = models.IntegerField(verbose_name = '代金券使用数量')

    class Meta:
        db_table = 'Payment'
        _description = '支付记录'

class Address(models.Model):
    province_id = models.IntegerField(verbose_name = '省', default = 0)
    #PROVINCE = ((0,'beijin'),)
    #CITY = ((0,'beijin'),(1,"shanghai"))
    city_id = models.IntegerField(verbose_name = '城市', default = 0)
    #DISTRICT = ((0,'beijin'))
    district_id = models.IntegerField(verbose_name = '区', default = 0)
    linkMan = models.CharField(verbose_name = '联系人', max_length = 15)
    address = models.CharField(verbose_name = '详细地址', max_length = 100)
    mobile = models.CharField(verbose_name = '电话号码', max_length = 40)
    code = models.CharField(verbose_name = '邮政编码', max_length = 20)
    isDefault = models.BooleanField(verbose_name = '默认地址')
    owner_type = models.SmallIntegerField(verbose_name = "被标注地址的类型eg:微信用户,订单")
    owner_id = models.IntegerField(verbose_name = "微信用户、订单的id")


class Coupons(models.Model):
    name = models.CharField(verbose_name = '优惠券名称', max_length = 50)
    moneyMin = models.FloatField(verbose_name = '优惠券金额')
    moneyHreshold = models.FloatField(verbose_name = '满 减 最低额度')
    DATE_END_TYPE = ((0,"截止某日前有效"),(1,"领取后有效时间倒计"))
    dateEndType = models.SmallIntegerField(verbose_name = '优惠券有效期类型', choices = DATE_END_TYPE)
    dateEndDays = models.DateTimeField(verbose_name = "优惠券截止时间", default = timezone.now)
    goods_id =  models.ForeignKey('Goods', on_delete = models.CASCADE, verbose_name = "商品id")
    is_active = models.BooleanField(verbose_name = "优惠券是否有效")
    date_add = models.DateTimeField(verbose_name = "优惠券添加的时间", default = timezone.now)
    coupons_type = models.SmallIntegerField(verbose_name = "优惠券类型1.通用型,2.分类专用型,3.商品专用型,4.店铺专用型", default = 0)

class Coupons_users(models.Model):
    coupons_id = models.IntegerField(verbose_name = "优惠券id")
    user_id = models.IntegerField(verbose_name = "用户id")
    date_add = models.DateTimeField(verbose_name = "优惠券添加的时间", default = timezone.now)
    dateEndDays = models.DateTimeField(verbose_name = "优惠券截止时间", default = timezone.now)
