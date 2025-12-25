from rest_framework import viewsets, permissions
from .models import Project, ProjectSite, ProjectMember, ProjectWBS
from .permissions import IsAdminManagerOrOwner
from .serializers import ProjectSerializer, ProjectCreateSerializer

from .serializers import (
    ProjectSerializer,
    ProjectSiteSerializer,
    ProjectMemberSerializer,
    ProjectWBSSerializer,
)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminManagerOrOwner]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return ProjectCreateSerializer
        return ProjectSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ProjectSiteViewSet(viewsets.ModelViewSet):
    queryset = ProjectSite.objects.all()
    serializer_class = ProjectSiteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        queryset = Project.objects.all()

        # Clients see only their projects
        if user.role == "CLIENT":
            queryset = queryset.filter(sponsor=user)

        # Filtering (status, sponsor)
        status = self.request.query_params.get("status")
        sponsor = self.request.query_params.get("sponsor")

        if status:
            queryset = queryset.filter(status=status)

        if sponsor:
            queryset = queryset.filter(sponsor_id=sponsor)

        return queryset

    def perform_create(self, serializer):
        serializer.save()


class ProjectMemberViewSet(viewsets.ModelViewSet):
    queryset = ProjectMember.objects.all()
    serializer_class = ProjectMemberSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProjectWBSViewSet(viewsets.ModelViewSet):
    queryset = ProjectWBS.objects.all()
    serializer_class = ProjectWBSSerializer
    permission_classes = [permissions.IsAuthenticated]
