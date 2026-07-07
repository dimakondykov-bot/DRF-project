from datetime import timedelta, timezone

from celery import shared_task
from users.models import User



@shared_task
def check_inactive_users():
    data_limit = timezone.now() - timedelta(days=30)
    users = User.objects.filter(last_login__lte=data_limit, is_active=True).update(is_active=False)
