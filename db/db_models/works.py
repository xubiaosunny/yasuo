from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _
from django.conf import settings


__all__ = ['Works', 'WorksComment', 'WorksQuestion', 'WorksQuestionReply']


class Works(models.Model):
    from .auth import CustomUser
    from .storage import LocalStorage

    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    type = models.CharField(_('Type'), max_length=50, null=True, blank=True)
    storage = models.ForeignKey(LocalStorage, on_delete=models.PROTECT)
    summary = models.TextField(_('Summary'), default='', blank=True)
    favorite = models.ManyToManyField(CustomUser, related_name='favorite_works')
    location = models.CharField(_('Location'), max_length=50, null=True, blank=True)
    create_time = models.DateTimeField(_('Create Time'), auto_now_add=True)
    is_delete = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Works')
        verbose_name_plural = _('Works')

    def details(self):
        data = dict()
        data['id'] = self.id
        data['user_id'] = self.user_id
        data['type'] = self.type
        data['storage'] = self.storage.details()
        data['summary'] = self.summary
        data['favorite_number'] = self.favorite.count()
        data['location'] = self.location
        data['create_time'] = self.create_time
        return data


class WorksComment(models.Model):
    from .auth import CustomUser
    from .storage import LocalStorage

    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    voice = models.ForeignKey(LocalStorage, on_delete=models.PROTECT)
    is_pay = models.BooleanField(default=False)
    create_time = models.DateTimeField(_('Create Time'), auto_now_add=True)
    update_time = models.DateTimeField(_('Update Time'), auto_now=True)

    class Meta:
        verbose_name = _('Works Comment')
        verbose_name_plural = _('Works Comment')


class WorksQuestion(models.Model):
    from .auth import CustomUser

    to = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    question = models.TextField(_('Question'))
    is_pay = models.BooleanField(default=False)
    create_time = models.DateTimeField(_('Create Time'), auto_now_add=True)

    class Meta:
        verbose_name = _('Works Question')
        verbose_name_plural = _('Works Question')


class WorksQuestionReply(models.Model):
    from .storage import LocalStorage

    works_question = models.ForeignKey(WorksQuestion, on_delete=models.PROTECT)
    voice = models.ForeignKey(LocalStorage, on_delete=models.PROTECT)
    create_time = models.DateTimeField(_('Create Time'), auto_now_add=True)

    class Meta:
        verbose_name = _('Works Question Reply')
        verbose_name_plural = _('Works Question Reply')
