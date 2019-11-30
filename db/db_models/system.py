from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _
from django.forms.models import model_to_dict


__all__ = ['AppUpdateLog', 'PriceSettings']


class AppUpdateLog(models.Model):
    SOURCE_CHOICES = (
        ('ios', _('ios')),
        ('android', _('android')),
    )

    source = models.CharField(_('Source'), max_length=50, choices=SOURCE_CHOICES)
    name = models.CharField(_('Name'), max_length=100)
    version = models.CharField(_('Version'), max_length=100)
    is_force = models.BooleanField(_('Is Force'))
    storage = models.ForeignKey('LocalStorage', on_delete=models.PROTECT)
    describe = models.TextField(_('Describe'))
    create_time = models.DateTimeField(_('Create Time'), auto_now_add=True)

    class Meta:
        verbose_name = 'App ' + _('Update')
        verbose_name_plural = 'App' + _('Update')

    def details(self):
        data = model_to_dict(self, exclude=['storage'])
        data['address'] = self.storage.file.url
        return data


class PriceSettings(models.Model):
    listen_comment = models.DecimalField(verbose_name=_("Listen Comment"), max_digits=12, decimal_places=2)
    listen_reply = models.DecimalField(verbose_name=_("Listen Reply"), max_digits=12, decimal_places=2)
    is_effective = models.BooleanField(verbose_name=_("Is Effective"), default=False)

    class Meta:
        verbose_name = _('Price Settings')
        verbose_name_plural = _('Price Settings')

    @staticmethod
    def current_price():
        price = PriceSettings.objects.filter(is_effective=True).order_by('-pk').first()
        return price or PriceSettings(listen_comment=0.01, listen_reply=0.01)

