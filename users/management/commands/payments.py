from django.core.management import BaseCommand
from materials.models import Course, Lesson
from users.models import User, Payments



class Command(BaseCommand):
    def handle(self, *args, **options):

        Payments.objects.all().delete()


        user = User.objects.first()
        course = Course.objects.first()
        lesson = Lesson.objects.first()

        Payments.objects.create(
            user=user,
            payments_date="2026-06-14",
            paid_course=course,
            payment_amount=15000.00,
            payment_method="cash"
        )


        Payments.objects.create(
            user=user,
            payments_date="2026-06-14",
            paid_lesson=lesson,
            payment_amount=1500.00,
            payment_method="transfer_to_account"
        )


        self.stdout.write(self.style.SUCCESS('База данных успешно наполнена платежами!'))
