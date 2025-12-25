from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DailyProgressViewSet, EVMSnapshotViewSet

router = DefaultRouter()
router.register(r"", DailyProgressViewSet, basename="progress")
router.register("evm", EVMSnapshotViewSet, basename="evm")
urlpatterns = [
    path("", include(router.urls)),
]
