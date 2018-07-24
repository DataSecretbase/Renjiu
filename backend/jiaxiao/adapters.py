from django.conf import setting
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class AccountAdapter(DefaultAccountAdapter):
	def is_open_for_signup(self, request):
		return getattr(settings, 'ACCOUNT_ALLOW_REGISTERATION', True)


class SocialAccountAdapter(DefaultSocialAccountAdpter):
	def is_open_for_signup(self, request, socaillogin):
		return getattr(settings, 'ACCOUNT_ALLOW_REGISTRATION', True)
