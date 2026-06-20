from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from materials.views import (
    LessonRetrieveAPIView,
    LessonDestroyAPIView,
    LessonUpdateAPIView,
    LessonCreateAPIView,
    LessonListAPIView,
    CourseViewSet,
)
from materials.apps import CourseConfig

app_name = CourseConfig.name

router = SimpleRouter()
router.register("courses", CourseViewSet, basename="users")

urlpatterns = [
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("lessons/", LessonListAPIView.as_view(), name="lesson-list"),
    path("lessons/create/", LessonCreateAPIView.as_view(), name="lesson-create"),
    path("lessons/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lesson-get"),
    path(
        "lessons/update/<int:pk>/", LessonUpdateAPIView.as_view(), name="lesson-update"
    ),
    path(
        "lessons/delete/<int:pk>/", LessonDestroyAPIView.as_view(), name="lesson-delete"
    ),
]

urlpatterns += router.urls
