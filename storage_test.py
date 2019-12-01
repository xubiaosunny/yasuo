import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yasuo.settings')

django.setup()

from db.models import LocalStorage
from utils.tasks import add_watermark, send_push_j

# storage = LocalStorage.objects.get(pk=1)
# add_watermark.delay(7)

send_push_j.delay('aaaaa')
