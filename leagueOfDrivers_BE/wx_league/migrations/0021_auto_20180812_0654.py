# Generated by Django 2.1 on 2018-08-12 06:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wx_league', '0020_auto_20180812_0641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordergoods',
            name='goods_id',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.SET_DEFAULT, to='wx_league.goods', verbose_name='商品id'),
        ),
    ]
