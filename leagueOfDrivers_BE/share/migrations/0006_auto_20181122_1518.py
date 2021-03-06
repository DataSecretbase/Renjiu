# Generated by Django 2.1.2 on 2018-11-22 15:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('share', '0005_auto_20181122_1443'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cash',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(verbose_name='提现金额')),
                ('add_time', models.DateField(auto_now_add=True, verbose_name='添加时间')),
                ('status', models.SmallIntegerField(choices=[(0, '待审核'), (1, '待打款'), (2, '已打款'), (3, '无效'), (4, '取消')], verbose_name='提现状态')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='share.ShareUser', verbose_name='用户')),
            ],
        ),
        migrations.AlterField(
            model_name='sharegoods',
            name='goods',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='wx_league.Goods', verbose_name='分销商品'),
        ),
    ]
