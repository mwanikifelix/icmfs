from apps.projects.models import Project


def get_project_metrics():
    """
    Project-related dashboard metrics
    """
    data = {
        "total": Project.objects.count(),
    }

    # Optional: status-based analytics (safe)
    if hasattr(Project, "status"):
        data["by_status"] = {
            status: Project.objects.filter(status=status).count()
            for status in Project.objects.values_list("status", flat=True).distinct()
        }

    return data
