# Generated by Django 2.1 on 2018-09-01 07:50

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wx_league', '0058_auto_20180901_0030'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.SmallIntegerField(verbose_name='预约时间')),
                ('num_student', models.SmallIntegerField(verbose_name='预约学生数量')),
                ('book_date', models.DateField(default=datetime.date(2018, 9, 1), verbose_name='预约设置的日期')),
                ('coachDriverSchool', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wx_league.CoachDriverSchool', verbose_name='教练所属驾校')),
            ],
            options={
                'verbose_name': '预约设置',
                'verbose_name_plural': '预约设置',
                'db_table': 'BookSet',
            },
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
    ]
