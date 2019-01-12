from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class StudyConfig(AppConfig):
    name = 'study'
    verbose_name = ('Обучение')

    def ready(self):
        import study.signals

