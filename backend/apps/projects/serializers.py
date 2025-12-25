from rest_framework import serializers
from .models import Project, ProjectSite, ProjectMember, ProjectWBS
from apps.accounts.models import User


class ProjectSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectSite
        fields = "__all__"


class ProjectSerializer(serializers.ModelSerializer):
    sites = ProjectSiteSerializer(many=True, read_only=True)
    sponsor_name = serializers.CharField(source="sponsor.username", read_only=True)

    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "sponsor",
            "sponsor_name",
            "status",
            "budget",
            "start_date",
            "end_date",
            "description",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]


class ProjectMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectMember
        fields = "__all__"


class ProjectWBSSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectWBS
        fields = "__all__"


class ProjectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            "name",
            "description",
            "sponsor",
            "budget",
            "start_date",
            "end_date",
        ]

    def validate_sponsor(self, value):
        if value.role != "CLIENT":
            raise serializers.ValidationError("Sponsor must be a CLIENT account.")
        return value
