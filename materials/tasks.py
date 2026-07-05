from celery import shared_task
from django.core.mail import send_mail
from materials.models import Course, Subscription



@shared_task
def send_course_update_email(course_id):
    course = Course.objects.get(id=course_id)
    email_list = []
    for sub in Subscription.objects.filter(course_id=course_id):
        email_list.append(sub.user.email)
    if email_list:
        send_mail(
            subject="Курс", message=f"Курс \"{course.title}\" был обновлён!", recipient_list=email_list,
        )



