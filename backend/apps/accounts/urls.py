from django.urls import path
from .views import RegisterView,  me, health


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import RegisterView, me, health

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("health/", health, name="accounts-health"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("me/", me),
]
