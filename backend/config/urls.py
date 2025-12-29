from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.http import JsonResponse

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


def health(request):
    return JsonResponse({"status": "ok"})


urlpatterns = [
    path(
        "api/v1/",
        include(
            [
                path("admin/", admin.site.urls),
                path("projects/", include("apps.projects.urls")),
                path("finance/", include("apps.finance.urls")),
                path("api/progress/", include("apps.progress.urls")),
                path("api/accounts/", include("apps.accounts.urls")),
                path("qa/", include("apps.qa.urls")),
                path("notifications/", include("apps.notifications.urls")),
            ]
        ),
    ),
    path("admin/", admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema")),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/accounts/", include("apps.accounts.urls")),
    path("api/projects/", include("apps.projects.urls")),
    path("api/progress/", include("apps.progress.urls")),
    path("api/finance/", include("apps.finance.urls")),
    #path("api/admin_panel/", include("apps.admin_panel.urls")),
    path("api/qa/", include("apps.qa.urls")),
    path("api/health/", lambda r: JsonResponse({"status": "ok"})),

    path("api/dashboard/", include("apps.dashboard.urls")),

    path("api/notifications/", include("apps.notifications.urls")),

]
