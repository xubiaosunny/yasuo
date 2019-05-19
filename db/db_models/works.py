from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _
from django.conf import settings


__all__ = ['Works']


class Works(models.Model):
    from .auth import CustomUser
    from .storage import LocalStorage

    user = models.OneToOneField(CustomUser, on_delete=models.PROTECT)
    storage = models.ForeignKey(LocalStorage, on_delete=models.PROTECT, null=True)
    summary = models.TextField(_('Summary'))
    location = models.CharField(_('Location'), max_length=50)
    create_time = models.DateTimeField(_('Create Time'), auto_now_add=True)
    is_delete = models.BooleanField(default=False)
