from celery import shared_task
import logging
from yasuo.config import J_PUSH
import jpush


__all__ = ['send_push_j']


_jpush = jpush.JPush(J_PUSH['appKey'], J_PUSH['masterSecret'])
_jpush.set_logging("DEBUG")


@shared_task
def send_push_j(message, alias=None):
    push = _jpush.create_push()
    push.audience = jpush.audience({"alias": alias}) if alias else jpush.all_

    push.notification = jpush.notification(alert=message)
    push.platform = jpush.all_
    push.send()
