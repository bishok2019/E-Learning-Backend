from apps.authentication.models.perms import CustomPermission, PermissionCategory, Roles
from apps.authentication.utils import PermissionLists
from base.views.generic_views import (
    CustomGenericCreateView,
    CustomGenericListView,
    CustomGenericRetrieveView,
    CustomGenericUpdateView,
)

from ..filters.roles import RolesFilter
from ..perms.custom_perms import (
    CustomAuthenticationPermission,
    CustomIsAuthenticatedPermission,
)
from ..serializers import (
    PermissionCategorySerializer,
    PermissionDropdownSerializer,
    PermissionSerializer,
    RolesCreateSerializer,
    RolesListSerializer,
    RolesListSerializerDropdown,
    RolesRetrieveSerializer,
    RolesUpdateSerializer,
)


class PermissionsListView(CustomGenericListView):
    queryset = CustomPermission.objects.all()
    serializer_class = PermissionSerializer
    filterset_fields = ["category"]
    success_response_message = "Permissions fetched successfully."

    def get_permissions(self):
        return [
            CustomAuthenticationPermission(
                models={
                    PermissionLists.HTTP_GET_METHOD: PermissionLists.CUSTOM_PERMISSION,
                },
            )
        ]


class PermissionsListDropdownView(CustomGenericListView):
    queryset = CustomPermission.objects.all()
    serializer_class = PermissionDropdownSerializer
    filterset_fields = ["category"]

    def get_permissions(self):
        return [CustomIsAuthenticatedPermission()]


class PermissionsCategoryListView(CustomGenericListView):
    queryset = PermissionCategory.objects.all()
    serializer_class = PermissionCategorySerializer
    success_response_message = "Permisssion Category fetched successfully."

    def get_permissions(self):
        return [
            CustomAuthenticationPermission(
                models={
                    PermissionLists.HTTP_GET_METHOD: PermissionLists.PERMISSION_CATEGORY,
                },
            )
        ]


class RolesListView(CustomGenericListView):
    queryset = Roles.objects.all().prefetch_related("permissions")
    serializer_class = RolesListSerializer
    success_response_message = "Roles fetched successfully."
    search_fields = ["name"]
    filterset_class = RolesFilter

    def get_permissions(self):
        return [
            CustomAuthenticationPermission(
                models={
                    PermissionLists.HTTP_GET_METHOD: PermissionLists.ROLES,
                },
            )
        ]


class RolesListDropdownView(CustomGenericListView):
    queryset = Roles.objects.all()
    serializer_class = RolesListSerializerDropdown

    def get_permissions(self):
        return [CustomIsAuthenticatedPermission()]


class RolesRetrieveView(CustomGenericRetrieveView):
    queryset = Roles.objects.all().prefetch_related("permissions")
    serializer_class = RolesRetrieveSerializer
    success_response_message = "Role retrieved successfully."

    def get_permissions(self):
        return [
            CustomAuthenticationPermission(
                models={
                    PermissionLists.HTTP_GET_METHOD: PermissionLists.ROLES,
                },
            )
        ]


class RolesCreateView(CustomGenericCreateView):
    queryset = Roles.objects.all()
    serializer_class = RolesCreateSerializer
    success_response_message = "Role created successfully."

    def get_permissions(self):
        return [
            CustomAuthenticationPermission(
                models={
                    PermissionLists.HTTP_POST_METHOD: PermissionLists.ROLES,
                },
            )
        ]


class RolesUpdateView(CustomGenericUpdateView):
    queryset = Roles.objects.all()
    serializer_class = RolesUpdateSerializer
    success_response_message = "Role updated successfully."

    def get_permissions(self):
        return [
            CustomAuthenticationPermission(
                models={
                    PermissionLists.HTTP_PATCH_METHOD: PermissionLists.ROLES,
                },
            )
        ]
