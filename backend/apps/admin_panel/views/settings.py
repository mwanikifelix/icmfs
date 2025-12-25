from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.admin_panel.services.audit import log_admin_action
from apps.admin_panel.models import AdminSetting
from apps.admin_panel.serializers import AdminSettingSerializer
from apps.admin_panel.models import SystemSetting
from apps.admin_panel.serializers import SystemSettingSerializer
from apps.admin_panel.permissions import IsSystemAdmin
from rest_framework.permissions import IsAuthenticated


class AdminSettingListView(APIView):
    permission_classes = [IsSystemAdmin]

    def get(self, request):
        settings = SystemSetting.objects.all()
        serializer = SystemSettingSerializer(settings, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SystemSettingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminSettingDetailView(APIView):
    permission_classes = [IsSystemAdmin]

    def put(self, request, pk):
        setting = SystemSetting.objects.get(pk=pk)
        serializer = SystemSettingSerializer(setting, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        SystemSetting.objects.get(pk=pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




class AdminSettingsView(APIView):
    permission_classes = [IsAuthenticated, IsSystemAdmin]

    def get(self, request):
        settings = SystemSetting.objects.all()
        serializer = AdminSettingSerializer(settings, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AdminSettingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save(updated_by=request.user)

        log_admin_action(
            user=request.user,
            action="UPDATE",
            resource="SystemSetting",
            metadata={"key": instance.key}
        )

        return Response(serializer.data)
