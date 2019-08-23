from celery import shared_task, task
from utils.core.jpush import push_message
from db.models import Message, Certification
import logging
import jpush
from django.utils.timezone import datetime


__all__ = ['send_push_j', 'teacher_station']


@shared_task
def send_push_j(user_id, message, class_name=None, class_id=None):
    logging.info(f"push params is user_id: {user_id}, message: {message}, class_name: {class_name}, class_id: {class_id}")
    res = push_message([user_id], message)
    if res:
        Message.objects.create(user_id=user_id, message=message, class_name=class_name, class_id=class_id)


@shared_task
def teacher_station():
    from db.models import CustomUser
    certifications = Certification.objects.filter(status=Certification.STATUS_CHOICES[1][0], push_time=None)
    for c in certifications:
        msg = '%s老师入驻啦' % (c.user.full_name or c.user.phone, )
        res = push_message(jpush.all_, msg)
        if res:
            c.push_time = datetime.now()
            c.save()
            querysetlist = []
            for user in CustomUser.objects.filter(is_active=True):
                querysetlist.append(Message(
                    user_id=user.id, message=msg, class_name=Message.CLASS_NAME_CHOICES[2][0], class_id=c.user_id))
            Message.objects.bulk_create(querysetlist)
