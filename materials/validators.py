from rest_framework import serializers

USER_LINK = "youtube.com"


def validate_link(value):
    if not value:
        return

    if USER_LINK not in value.lower():
        raise serializers.ValidationError(
            f"Неправильная ссылка. Разрешены только ссылки на {USER_LINK}"
        )
