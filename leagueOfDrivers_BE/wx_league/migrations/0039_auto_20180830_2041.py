# Generated by Django 2.1 on 2018-08-30 20:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wx_league', '0038_goodsreputation'),
    ]

    operations = [
        migrations.AddField(
            model_name='goodsreputation',
            name='user_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='评论用户'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='goodsreputation',
            name='goods_reputation_str',
            field=models.TextField(verbose_name='评论'),
        ),
        migrations.AlterField(
            model_name='wechatuser',
            name='avatar',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='wx_league.Icon', verbose_name='头像'),
        ),
    ]
