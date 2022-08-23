from django.apps import AppConfig
# from django.core.signals import request_finished


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        from api import signals # noqa
