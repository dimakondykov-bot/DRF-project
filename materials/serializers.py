from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from materials.models import Course, Lesson
from users.models import Payments


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseDetailSerializer(serializers.ModelSerializer):
    number_of_lessons= SerializerMethodField()

    def get_number_of_lessons(self, obj):
        return obj.lessons.count()

    lessons =LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ("name","description", "lessons","number_of_lessons")


