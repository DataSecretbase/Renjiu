from django.apps import AppConfig, apps


class WxLeagueConfig(AppConfig):
    name = 'wx_league'
    verbose_name = '驾校微信小程序'

    def ready(self):
        from actstream import registry
        registry.register(apps.get_model('wx_league', 'WechatUser'))