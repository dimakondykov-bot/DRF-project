from rest_framework import serializers
from rest_framework.serializers import ValidationError

user_link = "youtube.com"


def validate_link(value):
    if not value:
        return

    if "youtube.com" not in value.lower():
        raise serializers.ValidationError("не правилғнаә ссылка")
