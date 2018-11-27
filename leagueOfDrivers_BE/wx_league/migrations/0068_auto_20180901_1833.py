# Generated by Django 2.1 on 2018-09-01 18:33

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wx_league', '0067_auto_20180901_1130'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='isDefault',
            new_name='is_default',
        ),
        migrations.RenameField(
            model_name='address',
            old_name='linkMan',
            new_name='link_man',
        ),
        migrations.RenameField(
            model_name='bargain',
            old_name='minPrice',
            new_name='min_price',
        ),
        migrations.RenameField(
            model_name='bargainfriend',
            old_name='bargainFriend_id',
            new_name='bargain_friend_id',
        ),
        migrations.RenameField(
            model_name='bargainfriend',
            old_name='bargainUser_id',
            new_name='bargain_user_id',
        ),
        migrations.RenameField(
            model_name='bargainfriend',
            old_name='dateAdd',
            new_name='date_add',
        ),
        migrations.RenameField(
            model_name='bookset',
            old_name='coachDriverSchool',
            new_name='coach_driver_school',
        ),
        migrations.RenameField(
            model_name='coupons',
            old_name='dateEndDays',
            new_name='date_end_days',
        ),
        migrations.RenameField(
            model_name='coupons',
            old_name='dateEndType',
            new_name='date_end_type',
        ),
        migrations.RenameField(
            model_name='coupons',
            old_name='moneyHreshold',
            new_name='money_hreshold',
        ),
        migrations.RenameField(
            model_name='coupons',
            old_name='moneyMin',
            new_name='money_min',
        ),
        migrations.RenameField(
            model_name='coupons_users',
            old_name='dateEndDays',
            new_name='date_end_days',
        ),
        migrations.RenameField(
            model_name='goods',
            old_name='dateAdd',
            new_name='date_add',
        ),
        migrations.RenameField(
            model_name='goods',
            old_name='dateStart',
            new_name='date_start',
        ),
        migrations.RenameField(
            model_name='goods',
            old_name='dateUpdate',
            new_name='date_update',
        ),
        migrations.RenameField(
            model_name='goods',
            old_name='minScore',
            new_name='min_score',
        ),
        migrations.RenameField(
            model_name='goods',
            old_name='numberFav',
            new_name='number_fav',
        ),
        migrations.RenameField(
            model_name='goods',
            old_name='numberGoodReputation',
            new_name='number_good_reputation',
        ),
        migrations.RenameField(
            model_name='goods',
            old_name='numberOrders',
            new_name='number_orders',
        ),
        migrations.RenameField(
            model_name='goods',
            old_name='originalPrice',
            new_name='original_price',
        ),
        migrations.RenameField(
            model_name='goods',
            old_name='recommendStatus',
            new_name='recommend_status',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='dateAdd',
            new_name='date_add',
        ),
        migrations.RenameField(
            model_name='userexam',
            old_name='dateAdd',
            new_name='date_add',
        ),
        migrations.RenameField(
            model_name='userexam',
            old_name='dateEnd',
            new_name='date_end',
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
            model_name='bookset',
            name='book_date_end',
            field=models.DateTimeField(default=datetime.date(2018, 9, 1), verbose_name='预约设置结束的日期'),
        ),
        migrations.AlterField(
            model_name='bookset',
            name='book_date_start',
            field=models.DateTimeField(default=datetime.date(2018, 9, 1), verbose_name='预约设置开始的日期'),
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
