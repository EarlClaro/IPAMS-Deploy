from django.apps import AppConfig


class RecordsConfig(AppConfig):
    name = 'records'

    def ready(self):
        from . import scheduler
        scheduler.start()
