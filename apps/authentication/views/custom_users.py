from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import generics, status
from rest_framework.exceptions import NotFound
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenRefreshView

from apps.authentication.models.custom_users import CustomUser
from base.views.generic_views import (
    CustomGenericCreateView,
    CustomGenericListView,
    CustomGenericRetrieveView,
    CustomGenericUpdateView,
)

from ..serializers import (
    ChangePasswordSerializer,
    CustomUserCreateSerializer,
    CustomUserRetrieveSerializer,
    CustomUserUpdateSerializer,
    LoginSerializer,
    LogoutSerializer,
    UserListSerializer,
)

User = get_user_model()


class LogoutView(GenericAPIView):
    serializer_class = LogoutSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            return Response(
                {"message": "Logged out successfully."}, status=status.HTTP_200_OK
            )
        return Response(
            {"message": "Logout failed.", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class LoginView(GenericAPIView):
    permission_classes = []
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )

        from datetime import datetime

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        meta_data = {
            "timestamp": now,
        }
        if serializer.is_valid():
            return Response(
                {
                    "success": True,
                    "message": "Logged in successfully.",
                    "meta_data": meta_data,
                    **serializer.validated_data,
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {
                "success": False,
                "message": "Invalid Credentials.",
                "meta_data": meta_data,
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


class RefreshTokenView(TokenRefreshView):
    permission_classes = []


class UserCreateView(CustomGenericCreateView):
    serializer_class = CustomUserCreateSerializer
    queryset = User.objects.all()


class UserUpdateView(CustomGenericUpdateView):
    serializer_class = CustomUserUpdateSerializer
    queryset = User.objects.all()
    success_response_message = "User updated successfully."


class UserRetrieveView(CustomGenericRetrieveView):
    serializer_class = CustomUserRetrieveSerializer
    queryset = User.objects.all()
    success_response_message = "Users retrieved successfully."


class UserListView(CustomGenericListView):
    queryset = CustomUser.objects.all()
    serializer_class = UserListSerializer


class ChangeUserPasswordView(CustomGenericUpdateView):
    serializer_class = ChangePasswordSerializer
    success_response_message = "Password changed successfully."
    queryset = User.objects.all()

    permission_classes = [
        IsAuthenticated,
    ]

    def get_object(self):
        user = self.request.user
        self.kwargs["user"] = user
        return user
