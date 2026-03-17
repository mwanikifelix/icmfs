



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

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
        qs = User.objects.all().order_by("username")

        # Optional filters from query params
        role   = request.query_params.get("role")
        status_ = request.query_params.get("status")   # "active" | "inactive"
        search = request.query_params.get("search")

        if role:
            qs = qs.filter(role=role)
        if status_ == "active":
            qs = qs.filter(is_active=True)
        elif status_ == "inactive":
            qs = qs.filter(is_active=False)
        if search:
            qs = qs.filter(username__icontains=search)   \
                 | qs.filter(email__icontains=search)    \
                 | qs.filter(first_name__icontains=search) \
                 | qs.filter(last_name__icontains=search)

        serializer = AdminUserSerializer(qs, many=True)

        log_action(user=request.user, action="LIST_USERS", resource="User")

        return Response({"count": qs.count(), "results": serializer.data})

    def post(self, request):
        serializer = AdminUserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

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

        log_action(
            user=request.user,
            action="DELETE_USER",
            resource=f"User:{user.id}",
            metadata={"username": user.username},
        )

        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AdminUserResetPasswordView(APIView):
    """POST /api/admin/users/{pk}/reset-password/"""
    permission_classes = [IsSystemAdmin]

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        new_password = request.data.get("new_password")

        if not new_password:
            return Response(
                {"detail": "new_password is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if len(new_password) < 8:
            return Response(
                {"detail": "Password must be at least 8 characters."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(new_password)
        user.save()

        log_action(
            user=request.user,
            action="RESET_PASSWORD",
            resource=f"User:{user.id}",
            metadata={"username": user.username},
        )

        return Response({"detail": f"Password updated for {user.username}."})


class AdminUserToggleStatusView(APIView):
    """POST /api/admin/users/{pk}/toggle-status/"""
    permission_classes = [IsSystemAdmin]

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)

        if request.user.pk == user.pk:
            return Response(
                {"detail": "You cannot deactivate your own account."},
                status=status.HTTP_403_FORBIDDEN,
            )

        user.is_active = not user.is_active
        user.save()

        action = "ACTIVATE_USER" if user.is_active else "DEACTIVATE_USER"
        log_action(
            user=request.user,
            action=action,
            resource=f"User:{user.id}",
            metadata={"username": user.username, "is_active": user.is_active},
        )

        state = "activated" if user.is_active else "deactivated"
        return Response({
            "detail": f"User {user.username} {state}.",
            "is_active": user.is_active,
        })


class AdminUserStatsView(APIView):
    """GET /api/admin/users/stats/"""
    permission_classes = [IsSystemAdmin]

    def get(self, request):
        return Response({
            "total":    User.objects.count(),
            "active":   User.objects.filter(is_active=True).count(),
            "inactive": User.objects.filter(is_active=False).count(),
            "by_role": {
                role: User.objects.filter(role=role).count()
                for role, _ in User.ROLE_CHOICES
            },
        })