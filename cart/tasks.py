from celery import shared_task
from datetime import timedelta
from django.utils import timezone
from .models import Cart


@shared_task
def delete_old_carts():
    two_days_ago = timezone.now() - timedelta(days=2)
    Cart.objects.filter(completed=False, creation_time__lt=two_days_ago).delete()
    print("Working")
