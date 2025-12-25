# apps/admin_panel/views/roles.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.admin_panel.services.audit import log_admin_action


from apps.admin_panel.permissions import IsSystemAdmin
from apps.admin_panel.models import Role
from apps.admin_panel.serializers import RoleSerializer


class AdminRoleListView(APIView):
    permission_classes = [IsSystemAdmin]

    def get(self, request):
        roles = Role.objects.all()
        serializer = RoleSerializer(roles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
