from django.apps import AppConfig, apps


class BaseConfig(AppConfig):
    name = 'base'

    def ready(self):
        from actstream import registry
        registry.register(self.get_model('User'))
