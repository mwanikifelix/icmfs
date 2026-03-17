from rest_framework import serializers
from .models import Project, ProjectSite, ProjectMember, ProjectWBS, Region, County, SubCounty, Ward, ProjectSiteMedia


class RegionSerializer(serializers.ModelSerializer):
    county_count = serializers.IntegerField(source="counties.count", read_only=True)
    class Meta:
        model  = Region
        fields = ["id", "name", "code", "description", "is_active", "county_count"]


class CountySerializer(serializers.ModelSerializer):
    region_name = serializers.CharField(source="region.name", read_only=True)
    class Meta:
        model  = County
        fields = ["id", "name", "code", "region", "region_name", "is_active"]


class WardSerializer(serializers.ModelSerializer):
    sub_county_name = serializers.CharField(source="sub_county.name", read_only=True)
    county_name     = serializers.CharField(source="sub_county.county.name", read_only=True)
    class Meta:
        model  = Ward
        fields = ["id", "name", "code", "sub_county", "sub_county_name", "county_name", "is_active"]


class SubCountySerializer(serializers.ModelSerializer):
    county_name = serializers.CharField(source="county.name", read_only=True)
    class Meta:
        model  = SubCounty
        fields = ["id", "name", "code", "county", "county_name", "is_active"]


class ProjectSiteSerializer(serializers.ModelSerializer):
    county_name_display = serializers.SerializerMethodField()
    project_name        = serializers.CharField(source="project.name", read_only=True)

    class Meta:
        model  = ProjectSite
        fields = [
            "id", "uuid", "project", "project_name",
            "site_name", "county", "county_name_display",
            "sub_county", "ward",
            "town", "gps_latitude", "gps_longitude",
            "status", "created_at",
        ]

    def get_county_name_display(self, obj):
        if obj.county:
            return obj.county.name
        return obj.county_name or "—"

class ProjectMemberSerializer(serializers.ModelSerializer):
    username  = serializers.CharField(source="user.username",  read_only=True)
    full_name = serializers.SerializerMethodField()
    class Meta:
        model  = ProjectMember
        fields = ["id", "project", "user", "username", "full_name", "role", "assigned_at"]
        read_only_fields = ["assigned_at"]

    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}".strip() or obj.user.username


class ProjectWBSSerializer(serializers.ModelSerializer):
    class Meta:
        model  = ProjectWBS
        fields = "__all__"


class ProjectSerializer(serializers.ModelSerializer):
    sites              = ProjectSiteSerializer(many=True, read_only=True)
    members            = ProjectMemberSerializer(many=True, read_only=True)
    sponsor_name       = serializers.SerializerMethodField()
    created_by_name    = serializers.SerializerMethodField()
    status_display     = serializers.CharField(source="get_status_display",       read_only=True)
    category_display   = serializers.CharField(source="get_category_display",     read_only=True)
    owner_type_display = serializers.CharField(source="get_owner_type_display",   read_only=True)
    region_detail      = RegionSerializer(source="region", read_only=True)
    county_detail      = CountySerializer(source="county", read_only=True)

    class Meta:
        model  = Project
        fields = [
            "id", "name", "sponsor", "sponsor_name", "client_name",
            "status", "status_display", "owner_type", "owner_type_display",
            "region", "region_detail", "county", "county_detail",
            "sub_county", "ward",
            "category", "category_display", "sector",
            "budget", "progress", "start_date", "end_date", "description",
            "created_by", "created_by_name", "created_at", "updated_at",
            "sites", "members",
        ]
        read_only_fields = ["created_at", "updated_at", "created_by"]

    def get_sponsor_name(self, obj):
        if obj.sponsor:
            return f"{obj.sponsor.first_name} {obj.sponsor.last_name}".strip() or obj.sponsor.username
        return obj.client_name or "—"

    def get_created_by_name(self, obj):
        if obj.created_by:
            return f"{obj.created_by.first_name} {obj.created_by.last_name}".strip() or obj.created_by.username
        return "—"


class ProjectSiteMediaSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectSiteMedia
        fields = "__all__"

class ProjectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Project
        fields = [
            "name", "client_name", "sponsor",
            "status", "owner_type",
            "region", "county", "sub_county", "ward",
            "category", "sector",
            "budget", "progress", "start_date", "end_date", "description",
        ]
        extra_kwargs = {
            "sponsor":    {"required": False, "allow_null": True},
            "region":     {"required": False, "allow_null": True},
            "county":     {"required": False, "allow_null": True},
            "sub_county": {"required": False, "allow_null": True},
            "ward":       {"required": False, "allow_null": True},
            "owner_type": {"required": False, "allow_blank": True},
            "category":   {"required": False, "allow_blank": True},
            "sector":     {"required": False, "allow_blank": True},
            "end_date":   {"required": False, "allow_null": True},
            "budget":     {"required": False, "allow_null": True},
            "progress":   {"required": False},
        }
