from celery import shared_task
from utils.core.jpush import push_message
from db.models import Message
import logging

__all__ = ['send_push_j']


@shared_task
def send_push_j(user_id, message, class_name=None, class_id=None):
    logging.info(f"push params is user_id: {user_id}, message: {message}, class_name: {class_name}, class_id: {class_id}")
    res = push_message([user_id], message)
    if res:
        Message.objects.create(user_id=user_id, message=message, class_name=class_name, class_id=class_id)
