# Generated by Django 2.1 on 2018-08-12 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wx_league', '0021_auto_20180812_0654'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordergoods',
            name='goods_id',
            field=models.IntegerField(default=0, verbose_name='商品id'),
        ),
        migrations.AlterField(
            model_name='ordergoods',
            name='order_id',
            field=models.IntegerField(default=0, verbose_name='订单'),
        ),
    ]
