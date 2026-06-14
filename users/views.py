from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from users.models import User, Payments
from users.serializers import UserSerializer, PaymentsSerializer


class UsersViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PaymentsListApiView(generics.ListAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer

    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ("paid_course", "paid_lesson", "payment_method")
    ordering_fields = ("payments_date",)
