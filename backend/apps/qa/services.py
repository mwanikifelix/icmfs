def qa_summary(project):
    inspections = project.inspections.all()

    return {
        "total_inspections": inspections.count(),
        "approved": inspections.filter(status="approved").count(),
        "rejected": inspections.filter(status="rejected").count(),
        "rework_required": inspections.filter(status="rework").count(),
    }
