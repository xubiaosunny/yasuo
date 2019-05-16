from celery import shared_task
from db.models import LocalStorage

__all__ = ['add_watermark']


@shared_task
def add_watermark(storage: LocalStorage):
    path = storage.file.url
    if storage.type.startswith('image'):
        return add_watermark_for_image(path)
    elif storage.type.startswith('video'):
        return add_watermark_for_image(path)
    return False


def add_watermark_for_image(path):
    pass


def add_watermark_for_video(path):
    pass
