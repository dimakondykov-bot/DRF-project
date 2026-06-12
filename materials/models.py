from django.db import models


class Course(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Название курса",
        help_text="Введите название курса",
    )

    preview = models.ImageField(
        blank=True,
        null=True,
        max_length=150,
        upload_to="materials/photo",
        verbose_name="Картинка",
        help_text="Загрузите картинку",
    )

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание",
        help_text="Описание курса",
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="lessons",
        verbose_name="Курс",
    )

    name = models.CharField(
        max_length=150,
        verbose_name="Название урока",
        help_text="Введите название урока",
    )

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Урок",
        help_text="Описание урока",
    )

    preview = models.ImageField(
        blank=True,
        null=True,
        max_length=150,
        upload_to="materials/photo",
        verbose_name="Картинка",
        help_text="Загрузите картинку",
    )

    source_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="Ссылка на видео",
        help_text="Укажите ссылку на видеоматериал",
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return self.name
