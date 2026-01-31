from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .views import CustomAPIResponse


class CustomPagination(PageNumberPagination):
    page_size_query_param = "limit"

    # if limit ,page is not given then default pagination limit sets to 50
    page_size = 50

    # if limit > this. the qs are capped to max_page_size limit (threshold for limit)
    max_page_size = 50

    page_query_param = "page"

    def get_paginated_response(self, data):
        return Response(
            {
                "success": True,
                # "message": self.success_response_message,
                "message": getattr(
                    self, "success_response_message", "Data retrieved successfully."
                ),
                "total_count": self.page.paginator.count,
                "current_count": len(data),
                "total_pages": self.page.paginator.num_pages,
                "current_page": self.page.number,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "data": data,
            }
        )


class FilteringOrderingPaginationMixin:
    # Mixin to add filtering, ordering, and pagination to a view.

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = []
    ordering_fields = ["-created_at", "created_at", "id", "-id"]
    ordering = "-created_at"
    filterset_fields = []
    pagination_class = CustomPagination


class CustomErrorMessage:
    def _get_message(self, data):
        for field, errors in data.items():
            if isinstance(errors, list):
                for error in errors:
                    return f"Failed. {str(error).capitalize()}"
            elif isinstance(errors, str):
                return f"Failed. {errors.capitalize()}"
        return None


class CustomGenericListView(FilteringOrderingPaginationMixin, ListAPIView):
    request_action = "list"
    success_response_message = "Data retrieved successfully."

    def list(self, request, *args, **kwargs):
        if self.pagination_class and hasattr(self, "success_response_message"):
            setattr(
                self.pagination_class,
                "success_response_message",
                self.success_response_message,
            )
        return super().list(request, *args, **kwargs)


class CustomGenericCreateView(CreateAPIView, CustomErrorMessage):
    success_response_message = "Data created successfully."

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            errors = serializer.errors
            message = self._get_message(data=errors)
            if message:
                return CustomAPIResponse.custom_error_response(
                    errors=errors, message=message
                )
            return CustomAPIResponse.custom_error_response(
                errors=errors,
            )
        self.perform_create(serializer)
        return CustomAPIResponse.custom_success_response(
            data=serializer.data,
            message=self.success_response_message,
            status_code=status.HTTP_201_CREATED,
        )


class CustomGenericUpdateView(UpdateAPIView, CustomErrorMessage):
    http_method_names = ["patch"]  # only allows PATCH

    success_response_message = "Data updated successfully."

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if not serializer.is_valid():
            errors = serializer.errors
            message = self._get_message(data=errors)
            if message:
                return CustomAPIResponse.custom_error_response(
                    errors=errors, message=message
                )
            return CustomAPIResponse.custom_error_response(
                errors=errors,
            )

        self.perform_update(serializer)
        return CustomAPIResponse.custom_success_response(
            data=serializer.data, message=self.success_response_message
        )


class CustomGenericRetrieveView(RetrieveAPIView):
    success_response_message = "Data retrieved successfully."

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return CustomAPIResponse.custom_success_response(
            data=serializer.data, message=self.success_response_message
        )
