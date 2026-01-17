# apps/admin/views/roles.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from apps.admin.permissions import IsSystemAdmin
from apps.admin.models import Role
from apps.admin.serializers import RoleSerializer
from apps.admin.services.audit import log_action

User = get_user_model()


class AdminRoleListView(APIView):
    permission_classes = [IsSystemAdmin]

    def get(self, request):
        roles = Role.objects.all().order_by("name")
        serializer = RoleSerializer(roles, many=True)

        return Response(
            {
                "count": roles.count(),
                "results": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        serializer = RoleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        role_name = serializer.validated_data.get("name")

        # prevent duplicate role names
        if Role.objects.filter(name__iexact=role_name).exists():
            return Response(
                {"detail": "Role with this name already exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        role = serializer.save()

        # audit log
        log_action(
            user=request.user,
            action="CREATE",
            resource="ROLE",
            metadata={
                "role_id": role.id,
                "role_name": role.name,
            },
        )

        return Response(
            RoleSerializer(role).data,
            status=status.HTTP_201_CREATED,
        )


class AdminRoleDetailView(APIView):
    permission_classes = [IsSystemAdmin]

    def delete(self, request, pk):
        role = get_object_or_404(Role, pk=pk)

        # 🚨 prevent deleting roles in use
        if User.objects.filter(role=role).exists():
            return Response(
                {"detail": "Role is assigned to users and cannot be deleted"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        log_action(
            user=request.user,
            action="DELETE",
            resource="ROLE",
            metadata={
                "role_id": role.id,
                "role_name": role.name,
            },
        )

        role.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
