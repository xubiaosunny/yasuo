from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _
from django.conf import settings


__all__ = ['Works', 'WorksComment', 'WorksQuestion', 'WorksQuestionReply']


class Works(models.Model):
    from .auth import CustomUser
    from .storage import LocalStorage

    TYPE_CHOICES = (
        ('Drawing', _('Drawing')),
        ('Color', _('Color')),
        ('Sketch', _('Sketch')),
        ('Constitute', _('Constitute'))
    )

    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    type = models.CharField(_('Type'), choices=TYPE_CHOICES, max_length=50, null=True, blank=True)
    storage = models.ForeignKey(LocalStorage, on_delete=models.PROTECT)
    title = models.CharField(_('Title'), max_length=50, default='', blank=True)
    summary = models.TextField(_('Summary'), default='', blank=True)
    favorite = models.ManyToManyField(CustomUser, related_name='favorite_works')
    location = models.CharField(_('Location'), max_length=50, null=True, blank=True, db_index=True)
    create_time = models.DateTimeField(_('Create Time'), auto_now_add=True)
    is_ad = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Works')
        verbose_name_plural = _('Works')

    def details(self, user=None):
        data = dict()
        data['id'] = self.id
        data['user_id'] = self.user_id
        data['user'] = self.user.to_dict()
        data['type'] = self.type
        data['type_display'] = self.get_type_display()
        data['storage'] = self.storage.details()
        data['title'] = self.title
        data['summary'] = self.summary
        data['favorite_number'] = self.favorite.count()
        data['comment_number'] = self.workscomment_set.count()
        data['location'] = self.location
        data['create_time'] = self.create_time

        if user:
            data['is_favorite'] = self.favorite.filter(pk=user.id).exists()

        return data

    def mark_deleted(self):
        self.is_delete = True
        self.save()


class WorksComment(models.Model):
    from .auth import CustomUser
    from .storage import LocalStorage

    works = models.ForeignKey(Works, on_delete=models.PROTECT)
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    voice = models.ForeignKey(LocalStorage, on_delete=models.PROTECT)
    is_pay = models.BooleanField(default=False)
    create_time = models.DateTimeField(_('Create Time'), auto_now_add=True)
    update_time = models.DateTimeField(_('Update Time'), auto_now=True)

    class Meta:
        verbose_name = _('Works Comment')
        verbose_name_plural = _('Works Comment')

    def details(self):
        data = dict()
        data['id'] = self.id
        data['user'] = self.user.to_dict()
        # data['works'] = self.works.details()
        data['comment'] = self.voice.details()
        data['is_pay'] = self.is_pay
        data['create_time'] = self.create_time
        data['update_time'] = self.update_time
        return data


class WorksQuestion(models.Model):
    from .auth import CustomUser

    works = models.ForeignKey(Works, on_delete=models.PROTECT)
    to = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    question = models.TextField(_('Question'))
    is_pay = models.BooleanField(default=False)
    create_time = models.DateTimeField(_('Create Time'), auto_now_add=True)

    class Meta:
        verbose_name = _('Works Question')
        verbose_name_plural = _('Works Question')

    def details(self):
        data = dict()
        data['id'] = self.id
        # data['works'] = self.works.details()
        data['works_id'] = self.works_id
        data['to'] = self.to.to_dict()
        data['question'] = self.question
        data['is_pay'] = self.is_pay
        data['create_time'] = self.create_time
        return data


class WorksQuestionReply(models.Model):
    from .storage import LocalStorage

    works_question = models.ForeignKey(WorksQuestion, on_delete=models.PROTECT)
    voice = models.ForeignKey(LocalStorage, on_delete=models.PROTECT)
    create_time = models.DateTimeField(_('Create Time'), auto_now_add=True)

    class Meta:
        verbose_name = _('Works Question Reply')
        verbose_name_plural = _('Works Question Reply')

    def details(self):
        data = dict()
        data['id'] = self.id
        data['works_question'] = self.works_question_id
        data['voice'] = self.voice.details()
        data['create_time'] = self.create_time
        return data
