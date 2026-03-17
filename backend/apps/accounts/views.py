""" from multiprocessing import AuthenticationError
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
    }) """


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import generics, permissions, status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from .serializers import UserSerializer, RegisterSerializer
from .models import User


# ── Health check ──────────────────────────────────────────────
@api_view(["GET"])
@permission_classes([AllowAny])
def health(request):
    return Response({
        "service": "accounts",
        "status":  "ok",
        "message": "Backend is reachable",
    })


# ── Current user ──────────────────────────────────────────────
@api_view(["GET", "PATCH"])
@permission_classes([IsAuthenticated])
def me(request):
    """
    GET  /api/accounts/me/   → returns full user profile
    PATCH /api/accounts/me/  → updates own profile (name, phone, email)
    """
    user = request.user

    if request.method == "PATCH":
        # Users can only update these fields on themselves
        allowed = ["first_name", "last_name", "email", "phone"]
        data = {k: v for k, v in request.data.items() if k in allowed}
        serializer = UserSerializer(user, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user.refresh_from_db()

    return Response({
        "id":           user.id,
        "username":     user.username,
        "email":        user.email,
        "first_name":   user.first_name,
        "last_name":    user.last_name,
        "full_name":    f"{user.first_name} {user.last_name}".strip() or user.username,
        "phone":        user.phone,
        "role":         user.role,          # ✅ string e.g. "manager"
        "is_staff":     user.is_staff,
        "is_superuser": user.is_superuser,
        "is_active":    user.is_active,
        "date_joined":  user.date_joined,
        "last_login":   user.last_login,
    })


# ── Public registration ───────────────────────────────────────
class RegisterView(generics.CreateAPIView):
    """
    POST /api/accounts/register/
    Public self-registration. Role is always forced to 'client'.
    Admins use POST /api/admin/users/ to create users with other roles.
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Return JWT tokens immediately after registration
        refresh = RefreshToken.for_user(user)
        return Response({
            "access":  str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "id":         user.id,
                "username":   user.username,
                "email":      user.email,
                "first_name": user.first_name,
                "last_name":  user.last_name,
                "full_name":  f"{user.first_name} {user.last_name}".strip() or user.username,
                "role":       user.role,
            },
        }, status=status.HTTP_201_CREATED)