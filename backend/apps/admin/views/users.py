from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model

from apps.admin.permissions import IsSystemAdmin
from apps.admin.serializers import (
    AdminUserSerializer,
    AdminUserCreateSerializer,
)
from apps.admin.services.audit import log_action

User = get_user_model()


class AdminUserListView(APIView):
    permission_classes = [IsSystemAdmin]

    def get(self, request):
        users = User.objects.all().order_by("username")
        serializer = AdminUserSerializer(users, many=True)

        # ✅ AUDIT LOG — LIST USERS
        log_action(
            user=request.user,
            action="LIST_USERS",
            resource="User",
        )

        return Response(
            {
                "count": users.count(),
                "results": serializer.data,
            }
        )

    def post(self, request):
        serializer = AdminUserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        # ✅ AUDIT LOG — CREATE USER
        log_action(
            user=request.user,
            action="CREATE_USER",
            resource=f"User:{user.id}",
            metadata={"username": user.username},
        )

        return Response(
            AdminUserSerializer(user).data,
            status=status.HTTP_201_CREATED,
        )

from django.shortcuts import get_object_or_404


class AdminUserDetailView(APIView):
    permission_classes = [IsSystemAdmin]

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        return Response(AdminUserSerializer(user).data)

    def put(self, request, pk):
        user = get_object_or_404(User, pk=pk)

        if request.user.pk == user.pk:
            return Response(
                {"detail": "You cannot modify your own admin account"},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = AdminUserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # ✅ AUDIT LOG — UPDATE USER
        log_action(
            user=request.user,
            action="UPDATE_USER",
            resource=f"User:{user.id}",
            metadata={"username": user.username},
        )

        return Response(serializer.data)

    def delete(self, request, pk):
        user = get_object_or_404(User, pk=pk)

        if request.user.pk == user.pk:
            return Response(
                {"detail": "You cannot delete your own admin account"},
                status=status.HTTP_403_FORBIDDEN,
            )

        # ✅ AUDIT LOG — DELETE USER
        log_action(
            user=request.user,
            action="DELETE_USER",
            resource=f"User:{user.id}",
            metadata={"username": user.username},
        )

        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
