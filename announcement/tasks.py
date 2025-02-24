from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.utils import timezone


@shared_task
def update_expired_statuses():
    from .models import Product
    products = Product.objects.filter(expires_at__lte=timezone.now(), status=Product.Status.ACTIVE)

    for product in products:
        product.status = Product.Status.INACTIVE
        product.save()

    return f"Updated {len(products)} products"