from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from materials.models import Course, Subscription


@shared_task
def send_course_update_email(course_id):
    course = Course.objects.get(id=course_id)
    email_list = list(
        Subscription.objects.filter(course_id=course_id).values_list(
            "user__email", flat=True
        )
    )

    if email_list:
        send_mail(
            subject="Курс",
            message=f'Курс "{course.name}" был обновлён!',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=email_list,
        )
