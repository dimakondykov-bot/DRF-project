from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from users.models import Payments
from users.models import User


class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = "__all__"


class UserSerializer(ModelSerializer):
    payments = PaymentsSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ("id", "email", "password", "phone", "city", "avatar", "payments")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password", None)

        user = User.objects.create(**validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user

    def update(self, instance, validated_data):

        if "password" in validated_data:
            password = validated_data.pop("password")
            instance.set_password(password)

        return super().update(instance, validated_data)


class UserShortSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "phone", "city", "avatar")
