from celery import shared_task
from utils.core.jpush import push_message


__all__ = ['send_push_j']


@shared_task
def send_push_j(tags, message):
    push_message(tags, message)
