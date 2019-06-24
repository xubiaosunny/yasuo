from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

from django.utils import timezone
from django.forms.models import model_to_dict
from django.utils.translation import gettext as _


__all__ = ['CustomUser', 'Certification', 'SMSCode']


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
    ROLE_CHOICES = (
        ('T', _('Teacher')),
        ('S', _('Student')),
    )
    GRADE_CHOICES = (
        (10, _('grade ten')),
        (11, _('grade eleven')),
        (12, _('grade twelve')),
        (13, _('return students')),
    )

    phone = models.CharField(_('Phone Number'), max_length=100, unique=True)
    full_name = models.CharField(_('Full Name'), max_length=255, blank=True)
    is_active = models.BooleanField(_('active'), default=True, blank=True)
    is_admin = models.BooleanField(_('staff status'), default=False, blank=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now, blank=True)

    role = models.CharField(choices=ROLE_CHOICES, max_length=5, null=True, blank=True)
    province = models.CharField(_('province'), max_length=100, null=True, blank=True)
    city = models.CharField(_('city'), max_length=100, null=True, blank=True)
    avatar = models.ForeignKey('LocalStorage', default=None, null=True, blank=True, on_delete=models.PROTECT,
                               verbose_name=_('Avatar'))
    introduction = models.TextField(_('Introduction'), default='', blank=True)

    follow = models.ManyToManyField('self', symmetrical=False)
    credit = models.DecimalField(max_digits=19, decimal_places=3, default=0)

    # student info
    grade = models.IntegerField(choices=GRADE_CHOICES, null=True, blank=True)

    # teacher info
    work_place = models.CharField(_('Work Place'), max_length=255, default='', blank=True, db_index=True)

    objects = CustomUserManager()
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    class Meta:
        indexes = [
            models.Index(fields=['is_admin', 'role']),
        ]
        verbose_name = _('User')
        verbose_name_plural = _('User')

    def __str__(self):
        return '%s %s' % (self.full_name, self.phone)

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
        return self.full_name or self.phone

    def to_dict(self, detail=False, guest=None):
        data = model_to_dict(self, exclude=['password', 'follow', 'avatar'])
        data['avatar_url'] = self.avatar.file.url if self.avatar else ''
        if detail:
            data['my_follow'] = [u.to_dict() for u in self.follow.all()],
            data['follow_me'] = [u.to_dict() for u in self.customuser_set.all()]
        data['follow_me_count'] = self.customuser_set.count()
        if self.role == CustomUser.ROLE_CHOICES[0][0]:
            data['reply_question_count'] = self.worksquestion_set.count()
        else:
            data['question_count'] = sum([w.worksquestion_set.count() for w in self.works_set.filter(is_delete=False)])
        if guest:
            if guest.is_anonymous:
                data['is_followed'] = False
            else:
                data['is_followed'] = self.customuser_set.filter(pk=guest.id).exists()
        return data


class Certification(models.Model):
    from .storage import LocalStorage

    STATUS_CHOICES = (
        ('Verifying', _('Verifying')),
        ('Pass', _('Pass')),
        ('Reject', _('Reject')),
    )
    user = models.OneToOneField(CustomUser, on_delete=models.PROTECT)
    id_number = models.CharField(_('ID Number'), max_length=100, blank=True)
    certified_file = models.ForeignKey(LocalStorage, on_delete=models.PROTECT, null=True)
    status = models.CharField(_('Status'), choices=STATUS_CHOICES, max_length=20)
    reject_cause = models.TextField(_('Reject Cause'), default='', blank=True)
    create_time = models.DateTimeField(_('Create Time'), auto_now_add=True, blank=True)
    update_time = models.DateTimeField(_('Update Time'), auto_now=True, blank=True)

    class Meta:
        verbose_name = _('User Authentication')
        verbose_name_plural = _('User Authentication')

    def detail(self):
        data = model_to_dict(self, fields=['user', 'id_number', 'reject_cause'])
        data['certified_file'] = self.certified_file.get_url()
        return data


class SMSCode(models.Model):
    phone = models.CharField(_('Phone'), max_length=100)
    code = models.CharField(_('SMS Code'), max_length=20)
    send_time = models.DateTimeField(_('Send Time'), default=timezone.now)

    class Meta:
        indexes = [
            models.Index(fields=["phone", "send_time"]),
        ]

        verbose_name = _('SMS Code')
        verbose_name_plural = _('SMS Code')

    def is_expired(self):
        # a code will be invalid after 5 minutes
        return (timezone.now() - self.send_time).seconds > 300

    @staticmethod
    def is_invalid(phone, code):
        code_records = SMSCode.objects.filter(phone=phone)
        if code_records.count() == 0:
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
