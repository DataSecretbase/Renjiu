# Generated by Django 2.1.2 on 2018-11-26 11:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wx_league', '0104_auto_20181126_1106'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('share', '0010_auto_20181126_0537'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShareOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_goods', models.IntegerField(default=0, verbose_name='商品数量')),
                ('goods_price', models.FloatField(default=0, verbose_name='商品总金额')),
                ('total', models.FloatField(default=0, verbose_name='实际支付')),
                ('status', models.SmallIntegerField(choices=[(0, '待付款'), (1, '待发货'), (2, '待收货'), (3, '待评价'), (4, '已完成'), (5, '已删除')], default=0, verbose_name='状态')),
                ('remark', models.CharField(blank=True, max_length=100, verbose_name='备注')),
                ('linkman', models.CharField(blank=True, max_length=100, verbose_name='联系人')),
                ('phone', models.CharField(blank=True, max_length=50, verbose_name='手机号码')),
                ('province_id', models.SmallIntegerField(default=0, verbose_name='省')),
                ('city_id', models.SmallIntegerField(default=0, verbose_name='市')),
                ('district_id', models.SmallIntegerField(default=0, verbose_name='区')),
                ('address', models.CharField(blank=True, max_length=100, verbose_name='详细地址')),
                ('postcode', models.CharField(blank=True, max_length=20, verbose_name='邮政编码')),
                ('date_add', models.DateTimeField(auto_now_add=True, verbose_name='下单时间')),
                ('coupons', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='wx_league.Coupons', verbose_name='使用的优惠券')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='微信用户')),
            ],
            options={
                'verbose_name': '分销订单',
                'db_table': 'ShareOrder',
                'verbose_name_plural': '分销订单',
            },
        ),
        migrations.CreateModel(
            name='ShareOrderGoods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.IntegerField(default=0, verbose_name='订单')),
                ('goods_id', models.IntegerField(default=0, verbose_name='商品id')),
                ('name', models.CharField(blank=True, max_length=50, verbose_name='商品名称')),
                ('property_str', models.CharField(blank=True, max_length=200, verbose_name='商品规格')),
                ('price', models.FloatField(default=0, verbose_name='单价')),
                ('amount', models.IntegerField(default=0, verbose_name='商品数量')),
                ('total', models.FloatField(default=0, verbose_name='总价')),
                ('display_pic', models.ForeignKey(default=0, on_delete=django.db.models.deletion.SET_DEFAULT, to='wx_league.Icon', verbose_name='图片')),
            ],
            options={
                'verbose_name': '订单商品',
                'db_table': 'ShareOrderGoods',
                'verbose_name_plural': '订单商品',
            },
        ),
        migrations.AlterField(
            model_name='sharegoods',
            name='goods',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='wx_league.Goods', verbose_name='分销商品'),
        ),
    ]
