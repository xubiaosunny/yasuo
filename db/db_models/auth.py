from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

from django.utils import timezone
from django.utils.translation import gettext as _


class CustomUserManager(BaseUserManager):
    def create_user(self, phone, password=None):
        """
        Creates and saves a User with the given phone, date of
        birth and password.
        """
        if not phone:
            raise ValueError('Users must have an phone')

        user = self.model(phone=phone)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password):
        """
        Creates and saves a superuser with the given phone, date of
        birth and password.
        """
        user = self.create_user(
            phone,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    phone = models.CharField(_('Phone'), max_length=100, unique=True)
    name = models.CharField(_('name'), max_length=255, blank=True)
    is_active = models.BooleanField(_('active'), default=True, blank=True)
    is_admin = models.BooleanField(_('staff status'), default=False, blank=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now, blank=True)

    province = models.CharField(_('province'), max_length=100, null=True, blank=True)
    city = models.CharField(_('province'), max_length=100, null=True, blank=True)

    objects = CustomUserManager()
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def __str__(self):
        return '%s %s' % (self.name, self.phone)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def get_username(self):
        return self.name or self.phone


class SMSCode(models.Model):
    phone = models.CharField(_('Phone'), max_length=100)
    code = models.CharField(_('SMS Code'), max_length=20)
    send_time = models.DateTimeField(_('Send Time'), default=timezone.now)

    class Meta:
        index_together = ["phone", "send_time"]

    def is_expired(self):
        # a code will be invalid after 5 minutes
        return (timezone.now() - self.send_time).seconds > 300

    @staticmethod
    def is_invalid(phone, code):
        code_records = SMSCode.objects.filter(phone=phone)
        if code_records.count() == 0:
            print(1)
            return True
        last_record = code_records.order_by('-id').first()
        return last_record.is_expired() or last_record.code != code

    @staticmethod
    def get_last_in_one_minutes(phone):
        filter_time = timezone.now() - timezone.timedelta(minutes=1)
        code_records = SMSCode.objects.filter(phone=phone, send_time__gt=filter_time)
        if code_records.count() == 0:
            return None
        return code_records.order_by('-id').first()