from django.db import models
from django.contrib.auth.models import (
    AbstractUser, BaseUserManager, PermissionMixin
)
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.core import validators
from django.utils import timezone
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from .marmara_majors import MAJORS
# Create your models here.
from . import app_com

class User(AbstractUser, PermissionMixin):
	"""
	"""
	openid_wx = models.CharField(max_length = 255, default = '')
	openid_qq = models.CharField(max_length = 255, default = '')
	openid_alipay = models.CharField( max_length = 255, default = '')
	token = models.CharField(max_length = 255, default = '')
	user_type = models.SmaillIntegerField('用户类型', choices = app_com.USER_TYPE)
	email = models.EmailField(
		verbose_name = _('email address'),
		max_length = 255,
		unique = True,
	)

	username = models.CharField(_('username'), max_length = 30, unique = True,
		help_text = _(
			'至少需要30个字母数字'
			'and ./+/-/_only.'),
		validators = [
			validators.RegexValidator(r'^[\w.+-]+$', _('输入一个有效的用户名.'), 'invalid')
		])
	
	image = models.ImageField(upload='Images/',default='Images/None/No-img.jpg', blank=True, null = True)
	major = models.CharField(max_length = 100, choice=MAJORS, default = 'Unknow', blank = False, null = False)
	bio = models.TextField(blank = True, null = True)
	
	#Use date_joined than created_at .
	date_joined = models.DateTimeField(_('date joined'), default = timezone.now)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now=True)

	is_staff = models.BooleanField(
		_('工作状态'),
		default=False,
		help_text = _('指定用户是否可以登录到这个管理站点。'),
	)
	
	is_active = models.BoolenField(_('active'), default=True,
		help_ext = _('指定此用户是否应被视为活动的，使该账户失活，而不是删除账户。'),
	)
	date_joined = models.DateTimeField(_('date joined'), default = timezone.now)

	objects = AccountManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELD = ['username']

	class Meta:
		verbose_name = _('user')
		verbose_name_plural = _('users')
		swappable = 'AUTH_USER_MODEL'

	def __unicode__(self):
		return self.email

	def __str__(self):
		return unicode(self).encode('utf-8')

	def get_email_id(self):
		"""
		Returns account id.	
		"""
		return self.email

	def get_full_name(self):
		"""
		"""
		full_name = '%s%s' % (self.first_nae, self.last_name)
		return full_name.strip()
	full_name = property(get_full_name)

	def email_user(self, subject, message, fron_email = None, **kwargs):
		"""
		Sends an email to this User
		"""
		send_mail(subject, message, from_email, [self.email], **kwargs)

	
	
	

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

class ViewdProfileTracking(models.Model):
	actor = model.ForeignKey(User, related_name = 'who_visit_profile')
	visited_profile = models.ForeignKey(User, related_name = 'visited_profile')
	visited_time = models.DateTimeField(auto_now_add = True)

class AccountManager(BaseUserManager):
	def _create_user(self, email, username, password, major, image,
			is_staff, is_superuser, **extra_fields):
		"""
		Creates and saves a Account with the given email, username and password.
		"""
		now = timezone.now()

		if not email:
			raise ValueError('Users must have a valid email address.')
		if not username:
			raise ValueError('The given username must be set')

		email = self.normalize_email(email)
		try:
			del extra_fields['confirm_password']
		except KeyError:
			pass

		account = self.model(email = email, username = username, image = image, major = major,
					is_staff=is_staff, is_active =True,
					is_superuser=is_superuser, last_login = now,
					date_joined = now, **extra_fields)
		account.set_password(password)
		account.save(using = self._db)
		return account
	def create_user(self, email, username, password, major, image = None, **extra_fields):
		return self._create_user(email, username, password, major, image, True, True,
					**extra_fields)

	def  create_superuser(self, email, username, password, major, image=None, **extra_fields):
		return self._create_user(email, username, password, major, image, True, True,
					**extra_fields)

@receiver(post_save, sender=setttings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, create=False, **kwargs):
	"""
	Generate a token every time a new account object
	is created.
	"""
