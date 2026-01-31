from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from .utils import (
    HttpBasedPermissionActionMaps,
)


class CustomIsAuthenticatedPermission(IsAuthenticated):
    """
    A simple permission mixin that ensures the user is authenticated.
    used mostly in DropDown APIS
    """

    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False
        return True


class CustomAuthenticationPermission(IsAuthenticated):
    """
    Custom permission class that:
    - Checks if the user has required CRUD permissions for multiple models.
    - Supports custom action permissions like 'can_verify_product'.

    IMPORTANT : Either CRUD Models || CustomPermission  is used (Cant have Both && Must have atleast One)
    """

    def __init__(
        self,
        # for Non branch
        models: dict = None,
        custom_permission: tuple = None,
    ):
        """
        : models: Dict of HTTP ReqMethods with MODELS Name (as strings) for standard CRUD checks.
        This Data strucutre works for All types of view sets i.e. ModelViewSet , Generics , APIViews
        models = {
            'GET' : ModelsA,
            'PATCH' : ModelsA,
            }
        : custom_permission: Tuples strings representing a special action permission (e.g., 'can_verify_product','can_generate_invoice',etc).
        """
        # For Non Branch
        self.models = models
        self.custom_permission = custom_permission

    def get_permission_action(self, method: str) -> str:
        http_map = {
            "GET": HttpBasedPermissionActionMaps.CAN_VIEW,
            "POST": HttpBasedPermissionActionMaps.CAN_CREATE,
            "PUT": HttpBasedPermissionActionMaps.CAN_UPDATE,
            "PATCH": HttpBasedPermissionActionMaps.CAN_UPDATE,
            "DELETE": HttpBasedPermissionActionMaps.CAN_DELETE,
        }

        action = http_map.get(method, None)
        if action is None:
            raise PermissionDenied(f"Unsupported request method: {method}")

        return action

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        if not super().has_permission(request, view):
            return False

        # Ensure that at least one of models or custom_permission is provided
        if not self.models and not self.custom_permission:
            raise PermissionDenied(
                "Permission Denied! Either 'models' or 'custom_permission' must be provided in Permission Class"
            )
        if self.models and self.custom_permission:
            raise PermissionDenied(
                "Permission Denied! Only 'models' or 'custom_permission' must be provided in Permission Class"
            )

        self.request = request

    def non_branch_based_authentication(self):
        user_permissions = self.get_user_permissions()

        # if atleast 1 custom permission matches then we pass the authentication
        if self.custom_permission:
            for perm in self.custom_permission:
                if perm in user_permissions:
                    return True

            raise PermissionDenied(
                f"Permission denied. Missing Permissions: {self.custom_permission}"
            )

        http_method = str(self.request.method).upper()

        models_based_on_http_method = self.models.get(http_method, None)
        if models_based_on_http_method is None:
            raise PermissionDenied(
                f"Valid HTTP Request Method not Found: {http_method}"
            )

        # returns can_create , can_view
        action = self.get_permission_action(http_method)

        model_lower = str(models_based_on_http_method).lower()
        view_perm = f"{HttpBasedPermissionActionMaps.CAN_VIEW}_{model_lower}"
        create_perm = f"{HttpBasedPermissionActionMaps.CAN_CREATE}_{model_lower}"
        update_perm = f"{HttpBasedPermissionActionMaps.CAN_UPDATE}_{model_lower}"
        delete_perm = f"{HttpBasedPermissionActionMaps.CAN_DELETE}_{model_lower}"

        if action == HttpBasedPermissionActionMaps.CAN_CREATE:
            if create_perm not in user_permissions:
                raise PermissionDenied(
                    f"Permission denied. Missing permission : {delete_perm}"
                )

        elif action == HttpBasedPermissionActionMaps.CAN_UPDATE:
            if update_perm not in user_permissions:
                raise PermissionDenied(
                    f"Permission denied. Missing permission : {update_perm}"
                )

        elif action == HttpBasedPermissionActionMaps.CAN_DELETE:
            if delete_perm not in user_permissions:
                raise PermissionDenied(
                    f"Permission denied. Missing permission : {delete_perm}"
                )

        else:
            if (
                view_perm not in user_permissions
                and create_perm not in user_permissions
                and update_perm not in user_permissions
                and delete_perm not in user_permissions
            ):
                raise PermissionDenied(
                    f"Permission denied. Missing permission : {view_perm}"
                )

        return True
