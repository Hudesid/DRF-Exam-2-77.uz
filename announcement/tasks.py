from celery import shared_task
from celery.bin.control import status
from django.utils import timezone
from .models import Extra

@shared_task
def update_expired_statuses():
    expired_extras = Extra.objects.filter(expires_at__lte=timezone.now(), status__ne = 'not active')
    expired_extras.update(status='not active')