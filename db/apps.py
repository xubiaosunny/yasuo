from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DbConfig(AppConfig):
    name = 'db'
    verbose_name = _("Data")
