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
    def get_queryset(self):
        if self.request.user.groups.filter(name="Moderators").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=self.request.user)

    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    pagination_class = CastomPagination
class LessonRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner]


class SubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
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
