from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.validators import UniqueValidator

from materials.models import Course, Lesson, Subscription
from materials.validators import validate_link
from users.models import Payments


class CourseSerializer(serializers.ModelSerializer):

    is_subscribe = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    def get_is_subscribe(self, obj):
        user = self.context['request'].user

        if user.is_anonymous:
            return False

        return Subscription.objects.filter(user=user, course=obj).exists()


class LessonSerializer(serializers.ModelSerializer):

    source_url = serializers.URLField(validators=[validate_link], required=False)

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseDetailSerializer(serializers.ModelSerializer):

    number_of_lessons = SerializerMethodField()
    Lesson = LessonSerializer(many=True, read_only=True)
    is_subscribe = SerializerMethodField()

    def get_is_subscribe(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return Subscription.objects.filter(user=user, course=obj).exists()

    def get_number_of_lessons(self, obj):
        return obj.lessons.count()

    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ("name", "description", "lessons", "number_of_lessons")
