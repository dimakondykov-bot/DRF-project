from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from materials.models import Course, Lesson, Subscription
from materials.serializers import (
    LessonSerializer,
    CourseSerializer,
    CourseDetailSerializer,
)
from users.permissions import IsModerator, IsOwner
from rest_framework.permissions import IsAuthenticated
from materials.paginations import CastomPagination


class CourseViewSet(viewsets.ModelViewSet):
    """
    Комплексный контроллер для курсов.
    С помощью всего одного класса реализует полный набор CRUD-операций:
    Создание курса, Чтение списка, Просмотр деталей, Обновление и Удаление.
    """
    def get_queryset(self):
        if self.request.user.groups.filter(name="Moderators").exists():
            return Course.objects.all()
        return Course.objects.filter(owner=self.request.user)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseSerializer

    def get_permissions(self):
        if self.action == "create":
            if self.request.user.groups.filter(name="Moderators").exists():
                return [IsOwner()]
            return [IsAuthenticated()]
        elif self.action == "destroy":
            return [IsAuthenticated(), IsOwner()]
        elif self.action in ["retrieve", "update", "partial_update"]:
            return [IsAuthenticated(), IsOwner() | IsModerator()]
        else:
            return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    pagination_class = CastomPagination


class LessonCreateAPIView(generics.CreateAPIView):
    """
    Контроллер для создания нового урока.
    Принимает POST-запрос с данными урока и автоматически привязывает его к текущему пользователю.
    Модераторам доступ на создание закрыт.
    """
    def get_queryset(self):
        if self.request.user.groups.filter(name="Moderators").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=self.request.user)

    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.request.user.groups.filter(name="Moderators").exists():
            return [IsOwner()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListAPIView(generics.ListAPIView):
    """
    Контроллер для вывода списка всех уроков.
    Обычные пользователи видят только свои уроки, модераторы видят все.
    Вывод списка работает с пагинацией (разбивается на страницы).
    """
    def get_queryset(self):
        if self.request.user.groups.filter(name="Moderators").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=self.request.user)

    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    pagination_class = CastomPagination


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """
    Контроллер для детального просмотра одного урока по его ID.
    Доступен только авторизованным владельцам этого урока или модераторам.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    """
    Контроллер для редактирования/обновления данных урока по его ID.
    Вносить изменения могут владельцы или модераторы. Ссылки проверяются валидатором на YouTube.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    """
    Контроллер для удаления урока по его ID.
    Удалить урок может только создавший его пользователь. У модераторов прав на удаление нет.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner]


class SubscriptionAPIView(APIView):
    """
    Контроллер для управления подпиской на курсы.
    Работает как переключатель (toggle) для авторизованных пользователей.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Принимает ID курса в POST-запросе.
        Если подписка уже существует в базе — удаляет её. Если подписки нет — создает новую.
        """
        user = request.user

        course_id = request.data.get("course")
        course_item = get_object_or_404(Course, id=course_id)

        subscription_item = Subscription.objects.filter(course=course_item, user=user)

        if subscription_item.exists():
            subscription_item.delete()
            message = "Подписка удалена"
        else:
            Subscription.objects.create(course=course_item, user=user)
            message = "Подписка добавлена"

        return Response({"message": message})
