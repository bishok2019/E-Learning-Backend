from datetime import datetime

from django.core.exceptions import ValidationError
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken


class CustomAPIResponse:
    # this is custom api response for success and error used in both API VIew and generic viewsets

    @staticmethod
    def custom_success_response(
        data=None, message="Success", detail=None, status_code=status.HTTP_200_OK
    ):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        meta_data = {
            "timestamp": now,
        }
        response = {
            "success": True,
            "message": message,
            "detail": detail,
            "data": data,
            "meta_data": meta_data,
        }
        return Response(response, status=status_code)

    @staticmethod
    def custom_error_response(
        message="An error occurred",
        errors=None,
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=None,
    ):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        meta_data = {
            "timestamp": now,
        }
        response = {
            "success": False,
            "message": message,
            "errors": errors or {},
            "detail": detail,
            "meta_data": meta_data,
        }
        return Response(response, status=status_code)


class BaseAPIView(CustomAPIResponse, APIView):
    serializer_class = None

    def handle_exception(self, exc):
        response = super().handle_exception(exc)
        if isinstance(exc, ValidationError):
            return self.custom_error_response(
                message="Validation failed.", errors=response.data
            )
        return response
