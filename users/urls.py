from rest_framework.routers import SimpleRouter
from users.apps import UsersConfig
from users.views import UsersViewSet

app_name = UsersConfig.name

router = SimpleRouter()
router.register(r"", UsersViewSet, basename="users")

urlpatterns = router.urls
