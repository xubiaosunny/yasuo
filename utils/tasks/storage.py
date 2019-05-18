from celery import shared_task
import logging
import time
import os
from PIL import Image
from django.conf import settings
from db.models import LocalStorage

__all__ = ['add_watermark']

WATERMARK_IMG = os.path.join(settings.STATIC_ROOT, 'image/watermark_1_x2.jpg')


@shared_task
def add_watermark(storage_id):
    try:
        storage = LocalStorage.objects.get(pk=storage_id)
    except Exception as e:
        logging.exception(e)
        return False
    if not os.path.exists(LocalStorage.WATERMARK_PATH):
        os.makedirs(LocalStorage.WATERMARK_PATH)

    if storage.type.startswith('image'):
        return add_watermark_for_image(storage)
    elif storage.type.startswith('video'):
        return add_watermark_for_image(storage)
    return False


def random_name():
    import random
    import string
    return "%d_%s" % (int(time.time()), ''.join(random.choices(string.ascii_letters + string.digits, k=6)))


def add_watermark_for_image(storage):
    try:
        im = Image.open(storage.file.path)
        mark = Image.open(WATERMARK_IMG)
    except Exception as e:
        logging.exception(e)
        return False
    layer = Image.new('RGBA', im.size, (0, 0, 0, 0))
    layer.paste(mark, (0, im.size[1] - mark.size[1]))
    out = Image.composite(layer, im, layer)

    for _ in range(3):
        name = '%s.jpg' % random_name()
        out_file = os.path.join(LocalStorage.WATERMARK_PATH, name)
        if not os.path.exists(out_file):
            out.save(out_file, 'jpeg')

            storage.watermarked_filename = name
            storage.save()
            return True
    return False


def add_watermark_for_video(storage):
    pass


