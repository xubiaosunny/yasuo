from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _
from django.conf import settings
import os


__all__ = ['LocalStorage']


def file_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/<file_type>/<filename>
    file_type = instance.type.split('/')[0] if instance.type else 'other'
    return '{0}/{1}'.format(file_type, filename)


class LocalStorage(models.Model):
    from .auth import CustomUser
    WATERMARK_DIR = '_storage'
    WATERMARK_PATH = os.path.join(settings.MEDIA_ROOT, WATERMARK_DIR)

    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    type = models.CharField(_('File Type'), max_length=50)
    file = models.FileField(_('File'), upload_to='storage')
    watermarked_filename = models.CharField(_('watermarked filename'), max_length=50, null=True, blank=True)
    create_time = models.DateTimeField(_('Create Time'), auto_now_add=True, blank=True)

    def details(self):
        data = dict()
        data['id'] = self.id
        data['user_id'] = self.user_id
        data['type'] = self.type
        data['name'] = self.file.name
        data['url'] = self.get_url()
        data['create_time'] = self.create_time
        return data

    def get_url(self):
        if self.watermarked_filename:
            return settings.MEDIA_URL + os.path.join(self.WATERMARK_DIR, self.watermarked_filename)
        else:
            return self.file.url
