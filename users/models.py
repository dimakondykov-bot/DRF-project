from django.contrib.auth.models import AbstractUser
from materials.models import Course, Lesson
from django.db import models


class User(AbstractUser):
    username = None

    email = models.EmailField(
        max_length=100, unique=True, verbose_name="Почта", help_text="Введите email"
    )
    phone = models.CharField(
        max_length=16,
        blank=True,
        null=True,
        verbose_name="Телефон",
        help_text="Введите номер телефона",
    )
    city = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name="Город",
        help_text="Введите город",
    )
    avatar = models.ImageField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name="Аватарка",
        help_text="Загрузите аватарку",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class Payments(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="payments",
        verbose_name="пользователь",
    )

    payments_date = models.DateField(
        verbose_name="Дата оплаты", help_text="Укажите дату проведения платежа"
    )

    paid_course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Курс оплачен",
    )

    paid_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Урок оплачен",
    )

    payment_amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Суммы оплаты"
    )

    PAYMENT_METHODS = [("cash", "Наличные"), ("transfer_to_account", "Перевод на счёт")]

    payment_method = models.CharField(
        max_length=50,
        choices=PAYMENT_METHODS,
        default="cash",
        verbose_name="Способ оплаты",
    )

class PaymentDetails(models.Model):
    amount = models.PositiveIntegerField(
        verbose_name = "Сумма",
        help_text = "Введите сумму",

    )

    session_id = models.CharField(

        max_length=255,
        blank=True,
        null=True,
        verbose_name="id_ сессии",
        help_text="Укажите id сессии",
    )

    link = models.URLField(
        max_length=400,
        blank=True,
        null=True,
        verbose_name="Ссылка на оплату",
        help_text="Укажите ссылку на оплату",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Пользователь",
        help_text="Укажите пользователя",
    )

    def __str__(self):
        return f"Сумма платежа {self.amount}"