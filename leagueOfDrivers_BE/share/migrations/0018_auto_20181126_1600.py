# Generated by Django 2.1.2 on 2018-11-26 16:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('share', '0017_auto_20181126_1545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sharegoods',
            name='goods',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='wx_league.Goods', verbose_name='分销商品'),
        ),
    ]
