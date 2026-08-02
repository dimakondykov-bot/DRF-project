from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson


class LessonTestCase(APITestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create(email="student_test@test.ru")
        self.user.set_password("testpassword12345")
        self.user.save()
        self.course = Course.objects.create(
            name="Тестовый курс", description="Описание", owner=self.user
        )

    def test_lesson_create(self):
        self.client.force_authenticate(user=self.user)

        data = {
            "name": "Тест1",
            "course": self.course.id,
            "source_url": "https://youtube.com",
        }

        response = self.client.post(
            "/materials/lessons/create/", data=data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 1)
        self.assertEqual(Lesson.objects.first().name, "Тест1")
