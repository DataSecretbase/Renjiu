# Generated by Django 2.1 on 2018-08-09 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wx_league', '0003_category_pid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wechatuser',
            name='name',
            field=models.CharField(blank=True, max_length=40, verbose_name='昵称'),
        ),
    ]
