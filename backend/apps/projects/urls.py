

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

from .views import (
    ProjectViewSet,
    ProjectSiteViewSet,
    ProjectMemberViewSet,
    ProjectWBSViewSet,
    RegionViewSet,
    CountyViewSet,
    SubCountyViewSet,
    WardViewSet,
    ProjectSiteMediaViewSet,
)

router = DefaultRouter()
router.register("projects",    ProjectViewSet,       basename="projects")
router.register("sites",       ProjectSiteViewSet,   basename="sites")
router.register("members",     ProjectMemberViewSet, basename="members")
router.register("wbs",         ProjectWBSViewSet,    basename="wbs")
router.register("regions",     RegionViewSet,        basename="regions")
router.register("counties",    CountyViewSet,        basename="counties")
router.register("subcounties", SubCountyViewSet,     basename="subcounties")
router.register("wards",       WardViewSet,          basename="wards")
router.register("media",  ProjectSiteMediaViewSet,  basename="media")
urlpatterns = [
    path("", include(router.urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)