from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users.apps import UsersConfig
from users.views import (
    PaymentsCreateApiView,
    PaymentsListApiView,
    UserCreateApiView,
    UsersViewSet,
)

app_name = UsersConfig.name

router = SimpleRouter()
router.register(r"", UsersViewSet, basename="users")

urlpatterns = [
    path("payments/", PaymentsListApiView.as_view(), name="payments_list"),
    path("register/", UserCreateApiView.as_view(), name="user_register"),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path(
        "payments/create/",
        PaymentsCreateApiView.as_view(),
        name="payments_create",
    ),
]

urlpatterns += router.urls
