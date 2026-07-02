from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import ModelViewSet
from users.models import User, Payments
from users.serializers import UserSerializer, PaymentsSerializer, UserShortSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from users.services import create_stripe_price, create_stripe_session, create_stripe_session, create_stripe_product


class UsersViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ["retrieve", "update", "partial_update"]:
            user_id_from_url = self.kwargs.get("pk")

            if str(user_id_from_url) == str(self.request.user.id):
                return UserSerializer
        return UserShortSerializer



class PaymentsListApiView(generics.ListAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer

    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ("paid_course", "paid_lesson", "payment_method")
    ordering_fields = ("payments_date",)


class UserCreateApiView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]



class PaymentsCreateApiView(generics.CreateAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        payment: Payments = serializer.save(user=self.request.user)

        if payment.paid_course:
            product_name = payment.paid_course.title
            product_description = getattr(payment.paid_course, 'description', '')
        elif payment.paid_lesson:
            product_name = payment.paid_lesson.title
            product_description = getattr(payment.paid_lesson, 'description', '')
        else:
            product_name = "Оплата обучения"
            product_description = ""

        stripe_product = create_stripe_product(product_name, product_description)
        stripe_price = create_stripe_price(stripe_product.id,payment.payment_amount)
        stripe_session = create_stripe_session(stripe_price.id)

        payment.session_id = stripe_session.id
        payment.link = stripe_session.url

        payment.save()