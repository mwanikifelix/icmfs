from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from apps.admin.permissions import IsSystemAdmin
from apps.admin.models import SystemSetting
from apps.admin.serializers import SystemSettingSerializer
from apps.admin.services.audit import log_action


class AdminSettingListView(APIView):
    permission_classes = [IsSystemAdmin]

    def get(self, request):
        settings = SystemSetting.objects.all().order_by("key")
        serializer = SystemSettingSerializer(settings, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SystemSettingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = serializer.save(updated_by=request.user)

        # audit log
        log_action(
            user=request.user,
            action="CREATE",
            resource="SYSTEM_SETTING",
            metadata={"key": instance.key},
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AdminSettingDetailView(APIView):
    permission_classes = [IsSystemAdmin]

    def put(self, request, pk):
        setting = get_object_or_404(SystemSetting, pk=pk)
        serializer = SystemSettingSerializer(
            setting, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)

        instance = serializer.save(updated_by=request.user)

        # audit log
        log_action(
            user=request.user,
            action="UPDATE",
            resource="SYSTEM_SETTING",
            metadata={"key": instance.key},
        )

        return Response(serializer.data)

    def delete(self, request, pk):
        setting = get_object_or_404(SystemSetting, pk=pk)

        log_action(
            user=request.user,
            action="DELETE",
            resource="SYSTEM_SETTING",
            metadata={"key": setting.key},
        )

        setting.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AdminSettingsView(APIView):
    """
    Backward-compatible endpoint for admin UI
    (kept intentionally to avoid breaking frontend)
    """
    permission_classes = [IsSystemAdmin]

    def get(self, request):
        settings = SystemSetting.objects.all().order_by("key")
        serializer = SystemSettingSerializer(settings, many=True)
        return Response(serializer.data)
