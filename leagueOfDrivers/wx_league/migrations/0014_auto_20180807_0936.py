# Generated by Django 2.1 on 2018-08-07 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wx_league', '0013_auto_20180807_0928'),
    ]

    operations = [
        migrations.AddField(
            model_name='goods',
            name='recommendStatusStr',
            field=models.CharField(default='', max_length=10, verbose_name='推荐状态(文字)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='goods',
            name='statusStr',
            field=models.CharField(default='', max_length=10, verbose_name='商品状态(文字)'),
            preserve_default=False,
        ),
    ]
