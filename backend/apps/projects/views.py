from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Project, ProjectSite, ProjectMember, ProjectWBS, Region, County, SubCounty, Ward, ProjectSiteMedia
from .serializers import (
    ProjectSerializer, ProjectCreateSerializer,
    ProjectSiteSerializer, ProjectMemberSerializer,
    ProjectWBSSerializer, RegionSerializer, CountySerializer,
    SubCountySerializer, WardSerializer, ProjectSiteMediaSerializer,
)


class RegionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset           = Region.objects.filter(is_active=True)
    serializer_class   = RegionSerializer
    permission_classes = [permissions.IsAuthenticated]


class CountyViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class   = CountySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs        = County.objects.filter(is_active=True).select_related("region")
        region_id = self.request.query_params.get("region")
        if region_id:
            qs = qs.filter(region_id=region_id)
        return qs


class SubCountyViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class   = SubCountySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs        = SubCounty.objects.filter(is_active=True).select_related("county")
        county_id = self.request.query_params.get("county")
        if county_id:
            qs = qs.filter(county_id=county_id)
        return qs


class WardViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class   = WardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs     = Ward.objects.filter(is_active=True).select_related("sub_county")
        sc_id  = self.request.query_params.get("sub_county")
        if sc_id:
            qs = qs.filter(sub_county_id=sc_id)
        return qs


class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends    = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields   = ["status", "region", "county", "category", "owner_type", "sector"]
    search_fields      = ["name", "client_name", "description"]
    ordering_fields    = ["created_at", "start_date", "name", "budget"]
    ordering           = ["-created_at"]

    def get_queryset(self):
        user = self.request.user
        qs   = Project.objects.select_related("region", "county", "sponsor", "created_by") \
                              .prefetch_related("sites", "members__user")
        if user.role == "client" and not user.is_staff:
            qs = qs.filter(sponsor=user)
        return qs

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return ProjectCreateSerializer
        return ProjectSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ProjectSiteViewSet(viewsets.ModelViewSet):
    serializer_class   = ProjectSiteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs         = ProjectSite.objects.select_related("county").all()
        project_id = self.request.query_params.get("project")
        if project_id:
            qs = qs.filter(project_id=project_id)
        return qs


class ProjectMemberViewSet(viewsets.ModelViewSet):
    serializer_class   = ProjectMemberSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs         = ProjectMember.objects.select_related("user", "project").all()
        project_id = self.request.query_params.get("project")
        if project_id:
            qs = qs.filter(project_id=project_id)
        return qs


class ProjectWBSViewSet(viewsets.ModelViewSet):
    serializer_class   = ProjectWBSSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs         = ProjectWBS.objects.all()
        project_id = self.request.query_params.get("project")
        if project_id:
            qs = qs.filter(project_id=project_id)
        return qs


class ProjectSiteMediaViewSet(viewsets.ModelViewSet):

    queryset = ProjectSiteMedia.objects.all()
    serializer_class = ProjectSiteMediaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = ProjectSiteMedia.objects.select_related("project")

        project_id = self.request.query_params.get("project")

        if project_id:
            qs = qs.filter(project_id=project_id)

        return qs.order_by("-uploaded_at")

def create(self, request, *args, **kwargs):

    files = request.FILES.getlist("file")

    project_id = request.data.get("project")
    media_type = request.data.get("media_type")

    if not files:
        return Response(
            {"error": "No files uploaded"},
            status=status.HTTP_400_BAD_REQUEST
        )

    created = []

    for file in files:

        media = ProjectSiteMedia.objects.create(
            project_id=project_id,
            file=file,
            media_type=media_type,
            uploaded_by=request.user
        )

        created.append(media.id)

    return Response(
        {"uploaded": created},
        status=status.HTTP_201_CREATED
    )