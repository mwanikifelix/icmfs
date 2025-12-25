from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProjectViewSet,
    ProjectSiteViewSet,
    ProjectMemberViewSet,
    ProjectWBSViewSet,
)

router = DefaultRouter()
router.register("projects", ProjectViewSet, basename="projects")
router.register("sites", ProjectSiteViewSet)
router.register("members", ProjectMemberViewSet)
router.register("wbs", ProjectWBSViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
