# Generated by Django 2.1 on 2018-08-06 01:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wx_league', '0004_auto_20180806_0110'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='driverschool',
            name='cookie',
        ),
        migrations.AddField(
            model_name='wechatuser',
            name='cookie',
            field=models.CharField(default='', max_length=100, verbose_name='用户认证标识'),
        ),
    ]
