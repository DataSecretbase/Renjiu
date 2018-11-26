# Generated by Django 2.1.2 on 2018-11-26 15:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wx_league', '0106_auto_20181126_1149'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='wechatuser',
            managers=[
            ],
        ),
        migrations.RemoveField(
            model_name='wechatuser',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='wechatuser',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='wechatuser',
            name='is_staff',
        ),
        migrations.RemoveField(
            model_name='wechatuser',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='wechatuser',
            name='username',
        ),
        migrations.AlterField(
            model_name='attachment',
            name='owner_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wx_league.Goods', verbose_name='所属货物'),
        ),
        migrations.AlterField(
            model_name='bargain',
            name='goods_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wx_league.Goods', verbose_name='货物'),
        ),
        migrations.AlterField(
            model_name='coupons',
            name='goods_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wx_league.Goods', verbose_name='商品id'),
        ),
        migrations.AlterField(
            model_name='goodsreputation',
            name='goods_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wx_league.Goods', verbose_name='商品'),
        ),
        migrations.AlterField(
            model_name='wechatuser',
            name='email',
            field=models.EmailField(max_length=255, unique=True, verbose_name='email address'),
        ),
    ]
