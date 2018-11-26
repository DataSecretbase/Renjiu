from django.db import models
import django.utils.timezone as timezone
import random
import time
from uuid import uuid4
from datetime import datetime, date

import base.models as base


class Scheme(models.Model):
    index_pic = models.ForeignKey(base.Icon, verbose_name = "方案封面图", on_delete = models.SET_NULL,
            null = True, blank = True)
    title = models.CharField(verbose_name = "方案标题", max_length = 100)
    content = models.TextField(verbose_name = "方案内容")
    category_id = models.ForeignKey('Category', verbose_name = '方案分类',
            on_delete = models.SET_NULL, null = True, blank = True)
    editors = models.ForeignKey(base.User, verbose_name = "编辑者", on_delete = models.SET_NULL, null = True, blank = True)
    date_create = models.DateTimeField(verbose_name = "创建日期", auto_now_add = True)

    class Meta:
        db_table = "Scheme"
        verbose_name = '方案'
        verbose_name_plural = '方案'

class Category(models.Model):
    name = models.CharField(verbose_name='名称', max_length = 100)
    pid = models.ForeignKey('Category',
                            verbose_name='上级分类',
                            on_delete = models.SET_NULL,
                            null = True, blank = True)
    key = models.IntegerField(verbose_name='编号')
    is_use = models.BooleanField(verbose_name='是否启用', default=True)
    sort = models.IntegerField(verbose_name='排序')
    
    class Meta:
        db_table = 'FangAnCategory'
        verbose_name = '方案分类'
        verbose_name_plural = '方案分类'
    def __str__(self):
        return self.name
