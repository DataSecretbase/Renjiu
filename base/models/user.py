from django.db import models
from django.contrib.auth.models import AbstractUser
import django.utils.timezone as timezone
import random
import time
from uuid import uuid4
from datetime import datetime,date

from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.conf import settings
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.core import validators
from django.utils.translation import ugettext_lazy as _
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from ezhiGo import settings

#from .datasettings import league_model as m_set


def filepath(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid4().hex, ext)
    year = datetime.now().year
    month =datetime.now().month
    day = datetime.now().day
    return "img/{0}/{1}/{2}/{3}".format(year,month,day,filename)

class ImgField(models.ImageField):
    @property
    def url(self):
        self._require_file()
        return settings.domain_url + self.storage.url(self.name)

class Icon(models.Model):
   name = models.CharField(verbose_name = "图标名称", max_length = 20)
   display_pic = models.ImageField(verbose_name = "icon 对应",upload_to=filepath)
   date_add = models.DateTimeField(verbose_name = '上传时间', auto_now_add = True, null = True, blank = True)

   class Meta:
       db_table = 'Icon'
       verbose_name = '图标'
       verbose_name_plural = '图标'

   def __str__(self):
       return self.name


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """
    Generate a token every time a new account object
    is created.
    """
    if created:
        Token.objects.create(user=instance)


class AccountManager(BaseUserManager):
    def _create_user(self, email, username, password, image,
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

        account = self.model(email=email, username=username, image=image,
                             is_staff=is_staff, is_active=True,
                             is_superuser=is_superuser, last_login=now,
                             date_joined=now, **extra_fields)

        account.set_password(password)
        account.save(using=self._db)
        return account

    def create_user(self, email, username, password, image=None, **extra_fields):
        return self._create_user(email, username, password, image, False, False,
                                 **extra_fields)

    def create_superuser(self, email, username, password, image=None, **extra_fields):
        return self._create_user(email, username, password, image, True, True,
                                 **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(
        verbose_name=_('email address'),
        max_length=255,
        unique=True,
        blank = True,
        null = True
    )

    username = models.CharField(_('username'), max_length=30, unique=True,
                help_text=_('Required. 30 characters or fewer. Letters, digits'
                            ' and ./+/-/_ only.'),
                validators=[
                    validators.RegexValidator(r'^[\w.+-]+$', _('Enter a valid username jebal.'), 'invalid')
                ])

    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)

    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))

    image = models.ImageField(upload_to='Images/',default='Images/None/No-img.jpg', blank=True, null=True)
    # Use date_joined than created_at plz.
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        swappable = 'AUTH_USER_MODEL'

    
    def __str__(self):
        return self.email


    def get_email_id(self):
        """
        Returns account id.
        """
        return self.email

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()
    full_name = property(get_full_name)

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)


class ViewedProfileTracking(models.Model):
    actor = models.ForeignKey(User, related_name='who_visit_profile', on_delete = models.CASCADE)
    visited_profile = models.ForeignKey(User, related_name='visited_profile', on_delete = models.CASCADE)
    visited_time = models.DateTimeField(auto_now_add=True)
