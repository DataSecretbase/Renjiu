# Generated by Django 2.1 on 2018-08-27 20:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wx_league', '0031_auto_20180827_1556'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='book_time_end',
            field=models.IntegerField(default=datetime.datetime.now, verbose_name='预约结束时间'),
        ),
        migrations.AlterField(
            model_name='book',
            name='book_time_start',
            field=models.IntegerField(default=datetime.datetime.now, verbose_name='预约开始时间'),
        ),
    ]
