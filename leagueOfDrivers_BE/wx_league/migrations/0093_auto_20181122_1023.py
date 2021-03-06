# Generated by Django 2.1.2 on 2018-11-22 10:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wx_league', '0092_auto_20181003_2221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='owner_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wx_league.Goods', verbose_name='所属货物'),
        ),
        migrations.AlterField(
            model_name='bargain',
            name='calculate_method',
            field=models.SmallIntegerField(choices=[(0, 'line'), (1, 'log')], verbose_name='砍价计算模式'),
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
    ]
