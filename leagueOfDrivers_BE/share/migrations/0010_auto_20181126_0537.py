# Generated by Django 2.1.2 on 2018-11-26 05:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('share', '0009_auto_20181125_2137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cash',
            name='add_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='添加时间'),
        ),
        migrations.AlterField(
            model_name='sharegoods',
            name='goods',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='wx_league.Goods', verbose_name='分销商品'),
        ),
    ]
