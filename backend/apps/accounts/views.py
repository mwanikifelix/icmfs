from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView


from .serializers import UserSerializer, RegisterSerializer
from .models import User


@api_view(["GET"])
@permission_classes([AllowAny])
def health(request):
    return Response(
        {"service": "accounts", "status": "ok", "message": "Backend is reachable"}
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me_view(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
