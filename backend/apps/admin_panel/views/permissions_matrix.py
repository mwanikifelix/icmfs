from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.admin_panel.models import PermissionMatrix

class PermissionMatrixView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = PermissionMatrix.objects.all().values()
        return Response(data)

    def post(self, request):
        PermissionMatrix.objects.update_or_create(
            role=request.data["role"],
            permission=request.data["permission"],
            defaults={"allowed": request.data["allowed"]},
        )
        return Response({"status": "updated"})
