# Generated by Django 2.1 on 2018-08-09 23:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wx_league', '0004_auto_20180809_2313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wechatuser',
            name='avatar',
            field=models.ImageField(blank=True, upload_to='upload', verbose_name='头像'),
        ),
        migrations.AlterField(
            model_name='wechatuser',
            name='country',
            field=models.IntegerField(blank=True, default=0, verbose_name='国家'),
        ),
        migrations.AlterField(
            model_name='wechatuser',
            name='gender',
            field=models.SmallIntegerField(blank=True, default=0, verbose_name='gender'),
        ),
        migrations.AlterField(
            model_name='wechatuser',
            name='ip',
            field=models.CharField(blank=True, max_length=80, verbose_name='登陆IP'),
        ),
        migrations.AlterField(
            model_name='wechatuser',
            name='language',
            field=models.CharField(blank=True, max_length=40, verbose_name='语言'),
        ),
        migrations.AlterField(
            model_name='wechatuser',
            name='openid',
            field=models.CharField(blank=True, max_length=255, verbose_name='OpenId'),
        ),
        migrations.AlterField(
            model_name='wechatuser',
            name='phone',
            field=models.CharField(blank=True, max_length=50, verbose_name='手机号码'),
        ),
        migrations.AlterField(
            model_name='wechatuser',
            name='register_ip',
            field=models.CharField(blank=True, max_length=80, verbose_name='注册IP'),
        ),
        migrations.AlterField(
            model_name='wechatuser',
            name='union_id',
            field=models.CharField(blank=True, max_length=255, verbose_name='UnionId'),
        ),
    ]
