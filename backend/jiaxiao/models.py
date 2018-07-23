from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
from . import app_com

class User(AbstractUser):
	openid_wx = models.CharField(max_length = 255, default = '')
	openid_qq = models.CharField(max_length = 255, default = '')
	openid_alipay = models.CharField( max_length = 255, default = '')
	token = models.CharField(max_length = 255, default = '')
	user_type = models.SmaillIntegerField('用户类型', choices = app_com.USER_TYPE)

class Driverschool(models.Model):
	DScode = models.IntegerField('驾校识别码',)
	owner = models.ForeignKey('User', on_delete = models.CASCADE, verbose_name = '日志所属人', default = None)
	create_time = models.DateTimeField('驾校注册到APP的时间', auto_now_add = True)
	#日志类型
	last_active_time = models.DateTimeField('最后登录时间', auto_now = True)


class Log(models.Model):
	remotehost = models.CharField(max_length = 100 , default = '')
	userid = models.IntegerField('用户id')
	timestamp = models.DateTimeField('日志记录产生时间', auto_now = True)
	request_com = models.CharField('请求内容', choices = app_com.APP_COM, default = '')
	opt_type = models.CharField('操作类型', choices = app_com.OPT_TYPE, default = '')
