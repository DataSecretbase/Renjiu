from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone

import base.models as base

class IndexTopicQuerySet(models.QuerySet):
    def index(self):
        q = {}
        return self.all()

class IndexTopic(models.Model):
    topic = models.ForeignKey("Topic",verbose_name = "主题", on_delete = models.SET_NULL, null = True,
            blank = True)
    sorted_objects = IndexTopicQuerySet.as_manager()


class Topic(models.Model):
    title = models.CharField(max_length=100,verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    pic_index = models.ForeignKey("base.Icon",verbose_name = "首页图片", on_delete = models.SET_NULL,
            null = True, blank = True)
    node = models.ForeignKey("Node",verbose_name='所属节点', on_delete = models.SET_NULL,
            null = True, blank = True)
    author = models.ForeignKey(base.User,verbose_name='作者', on_delete = models.SET_NULL,
            null = True, blank = True)
    num_views = models.IntegerField(default=0,verbose_name='浏览量')
    num_comments = models.IntegerField(default=0,verbose_name='评论数')
    num_favorites = models.IntegerField(default=0,verbose_name='收藏数')
    last_reply = models.ForeignKey(base.User,related_name='+',verbose_name='最后回复者',
            on_delete = models.SET_NULL, null = True, blank = True)
    created_on = models.DateTimeField(auto_now_add=True,verbose_name='发表时间')
    updated_on = models.DateTimeField(blank=True, null=True,verbose_name='更新时间')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '主题'
        verbose_name_plural = '主题'

class Comment(models.Model):
    content = models.TextField(verbose_name='内容')
    author = models.ForeignKey(base.User,verbose_name='作者', on_delete = models.SET_NULL,
            null = True, blank = True)
    topic = models.ForeignKey(Topic,verbose_name='所属主题', on_delete = models.SET_NULL,
            null = True, blank = True)
    created_on = models.DateTimeField(auto_now_add=True,verbose_name='评论时间')

    def __str__(self):
        return self.content
    
    class Meta:
        verbose_name = '内容'
        verbose_name_plural = '内容'

class Node(models.Model):
    name = models.CharField(max_length=100,verbose_name='节点名称')
    slug = models.SlugField(max_length=100,verbose_name='url标识符')
    created_on = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    updated_on = models.DateTimeField(blank=True, null=True,auto_now=True,verbose_name='更新时间')
    num_topics = models.IntegerField(default=0,verbose_name='主题数')
    category = models.ForeignKey("Category",verbose_name='所属类别', on_delete = models.SET_NULL,
            null = True, blank = True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '节点'
        verbose_name_plural = '节点'

class Category(models.Model):
    name = models.CharField(max_length=100,verbose_name='类别名称')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = '分类'
