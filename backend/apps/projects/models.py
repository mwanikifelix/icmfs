import uuid
from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Region(models.Model):
    name        = models.CharField(max_length=100, unique=True)
    code        = models.CharField(max_length=20, unique=True, blank=True)
    description = models.TextField(blank=True)
    is_active   = models.BooleanField(default=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "project_regions"
        ordering = ["name"]

    def __str__(self):
        return self.name


class County(models.Model):
    name      = models.CharField(max_length=100, unique=True)
    code      = models.CharField(max_length=10, unique=True, blank=True)
    region    = models.ForeignKey(
        Region, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="counties",
    )
    is_active  = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "project_counties"
        ordering = ["name"]
        verbose_name_plural = "counties"

    def __str__(self):
        return self.name


class SubCounty(models.Model):
    name      = models.CharField(max_length=100)
    code      = models.CharField(max_length=20, blank=True)
    county    = models.ForeignKey(
        County, on_delete=models.CASCADE, related_name="subcounties",
    )
    is_active  = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table        = "project_subcounties"
        ordering        = ["name"]
        unique_together = ("name", "county")
        verbose_name_plural = "sub counties"

    def __str__(self):
        return f"{self.name} ({self.county.name})"


class Ward(models.Model):
    name       = models.CharField(max_length=100)
    code       = models.CharField(max_length=20, blank=True)
    sub_county = models.ForeignKey(
        SubCounty, on_delete=models.CASCADE, related_name="wards",
    )
    is_active  = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table        = "project_wards"
        ordering        = ["name"]
        unique_together = ("name", "sub_county")

    def __str__(self):
        return f"{self.name} ({self.sub_county.name})"


class Project(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)

    sponsor = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="owned_projects",
        null=True, blank=True,
    )
    client_name = models.CharField(max_length=255, blank=True)

    STATUS_CHOICES = [
        ("planned",     "Planned"),
        ("active",      "Active"),
        ("on_hold",     "On Hold"),
        ("at_risk",     "At Risk"),
        ("completed",   "Completed"),
        ("closed",      "Closed"),
        ("in_progress", "In Progress"),
        ("cancelled",   "Cancelled"),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="planned")

    OWNER_TYPE_CHOICES = [
        ("government",  "Government"),
        ("private",     "Private"),
        ("ngo",         "NGO"),
        ("ppp",         "Public–Private Partnership"),
        ("faith_based", "Faith-Based / CBO"),
        ("other",       "Other"),
    ]
    owner_type = models.CharField(max_length=30, choices=OWNER_TYPE_CHOICES, blank=True)

    region = models.ForeignKey(
        Region, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="projects",
    )
    county = models.ForeignKey(
        County, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="projects",
    )
    sub_county = models.ForeignKey(
        SubCounty, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="projects",
    )
    ward = models.ForeignKey(
        Ward, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="projects",
    )

    CATEGORY_CHOICES = [
        ("affordable_housing", "Affordable Housing"),
        ("infrastructure",     "Infrastructure"),
        ("commercial",         "Commercial"),
        ("residential",        "Residential"),
        ("mixed_use",          "Mixed-Use"),
        ("health",             "Health"),
        ("education",          "Education"),
        ("water_sanitation",   "Water & Sanitation"),
        ("energy",             "Energy"),
        ("ict",                "ICT"),
        ("trade",               "Trade"),
    ]
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, blank=True)

    SECTOR_CHOICES = [
        ("housing",        "Housing"),
        ("infrastructure", "Infrastructure"),
        ("health",         "Health"),
        ("education",      "Education"),
        ("commercial",     "Commercial"),
        ("water",          "Water & Sanitation"),
        ("energy",         "Energy"),
        ("transport",      "Transport"),
    ]
    sector   = models.CharField(max_length=30, choices=SECTOR_CHOICES, blank=True)
    budget   = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    progress = models.PositiveSmallIntegerField(default=0)

    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="created_projects",
    )
    start_date  = models.DateField()
    end_date    = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "projects"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class ProjectSite(models.Model):
    uuid      = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    project   = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="sites")
    site_name = models.CharField(max_length=255)
    county    = models.ForeignKey(
        County, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="sites",
    )
    sub_county = models.ForeignKey(
        SubCounty, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="sites",
    )
    ward = models.ForeignKey(
        Ward, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="sites",
    )
    county_name   = models.CharField(max_length=100, blank=True)
    town          = models.CharField(max_length=100, blank=True)
    gps_latitude  = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    gps_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    status        = models.CharField(max_length=20, default="active")
    created_at    = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.site_name


class ProjectMember(models.Model):
    ROLE_CHOICES = (
        ("engineer",   "Engineer"),
        ("architect",  "Architect"),
        ("consultant", "Consultant"),
        ("accountant", "Accountant"),
        ("manager",    "Project Manager"),
        ("owner",      "Owner"),
    )
    project     = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="members")
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    role        = models.CharField(max_length=30, choices=ROLE_CHOICES)
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("project", "user")

class ProjectSiteMedia(models.Model):

    MEDIA_TYPE_CHOICES = [
        ("photo", "Photo"),
        ("video", "Video"),
        ("document", "Document"),
    ]

    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="media",
    )

    site = models.ForeignKey(
        ProjectSite,
        on_delete=models.CASCADE,
        related_name="media",
        null=True,
        blank=True,
    )

    file = models.FileField(upload_to="project_media/")

    media_type = models.CharField(
        max_length=20,
        choices=MEDIA_TYPE_CHOICES,
    )

    caption = models.CharField(max_length=255, blank=True)

    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "project_site_media"
        ordering = ["-uploaded_at"]

    def __str__(self):
        return f"{self.media_type} - {self.project.name}"


class ProjectWBS(models.Model):
    uuid          = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    project       = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="wbs_items")
    wbs_code      = models.CharField(max_length=50)
    wbs_name      = models.CharField(max_length=255)
    description   = models.TextField(blank=True)
    planned_cost  = models.DecimalField(max_digits=15, decimal_places=2)
    planned_start = models.DateField()
    planned_end   = models.DateField()
    created_at    = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("project", "wbs_code")