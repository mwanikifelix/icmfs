from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.admin_panel.serializers import UserAdminSerializer
from apps.admin_panel.services.audit import log_admin_action

from django.contrib.auth import get_user_model
from apps.accounts.models import User
from apps.admin_panel.permissions import IsSystemAdmin
from apps.accounts.serializers import UserSerializer


User = get_user_model()

class AdminUserListView(APIView):
    permission_classes = [IsSystemAdmin]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


    def post(self, request):
        user = User.objects.create_user(
            username=request.data["username"],
            email=request.data.get("email"),
            password=request.data["password"]
        )
        log_admin_action(request.user, f"Created user {user.username}")
        return Response({"status": "created"})




class AdminUserCreateView(APIView):
    permission_classes = [IsSystemAdmin]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminUserDetailView(APIView):
    permission_classes = [IsSystemAdmin]

    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        return Response(UserSerializer(user).data)

    def put(self, request, pk):
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = User.objects.get(pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
