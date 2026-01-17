from multiprocessing import AuthenticationError
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import generics, permissions, status
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
def me(request):
    user = request.user

    return Response({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role,               # ✅ STRING
        "is_staff": user.is_staff,
        "is_superuser": user.is_superuser,
    })





class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response(
            {"detail": "Username and password required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = AuthenticationError(username=username, password=password)

    if user is None:
        return Response(
            {"detail": "Invalid username or password"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    refresh = RefreshToken.for_user(user)

    return Response({
        "access": str(refresh.access_token),
        "refresh": str(refresh),
        "user": {
            "id": user.id,
            "username": user.username,
            "is_staff": user.is_staff,
            "is_superuser": user.is_superuser,
        }
    })