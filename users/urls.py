from rest_framework.routers import SimpleRouter
from users.apps import UsersConfig
from users.views import UsersViewSet, PaymentsListApiView
from django.urls import path



app_name = UsersConfig.name

router = SimpleRouter()
router.register(r"", UsersViewSet, basename="users")

urlpatterns = [
    path("payments/", PaymentsListApiView.as_view(), name="payments_list"),
]

urlpatterns += router.urls

