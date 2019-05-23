from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _
from django.conf import settings


__all__ = ['Works', 'WorksComment', 'WorksAsk']


class Works(models.Model):
    from .auth import CustomUser
    from .storage import LocalStorage

    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    type = models.CharField(_('Type'), max_length=50, null=True, blank=True)
    storage = models.ForeignKey(LocalStorage, on_delete=models.PROTECT)
    summary = models.TextField(_('Summary'), default='', blank=True)
    location = models.CharField(_('Location'), max_length=50, null=True, blank=True)
    create_time = models.DateTimeField(_('Create Time'), auto_now_add=True)
    is_delete = models.BooleanField(default=False)


class WorksComment(models.Model):
    from .auth import CustomUser
    from .storage import LocalStorage

    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    voice = models.ForeignKey(LocalStorage, on_delete=models.PROTECT)
    is_pay = models.BooleanField(default=False)
    create_time = models.DateTimeField(_('Create Time'), auto_now_add=True)
    update_time = models.DateTimeField(_('Update Time'), auto_now=True)


class WorksQuestion(models.Model):
    from .auth import CustomUser
    to = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    question = models.TextField(_('Question'))
    create_time = models.DateTimeField(_('Create Time'), auto_now_add=True)


class WorksQuestionReply(models.Model):
    works_question = models.ForeignKey(WorksQuestion, on_delete=models.PROTECT)
    is_pay = models.BooleanField(default=False)
    create_time = models.DateTimeField(_('Create Time'), auto_now_add=True)
