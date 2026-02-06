from django.core.cache import cache

from apps.authentication.models.perms import CustomPermission


class PermissionLists:
    """
    Permissions Lists for Each APIS
    eg : Products AIO Create needs create permissions for Product,ProductCategory and Other related fields
    """

    HTTP_GET_METHOD = "GET"
    HTTP_POST_METHOD = "POST"
    HTTP_PATCH_METHOD = "PATCH"
    # HTTP_PUT_METHOD = "PUT"
    # HTTP_DELETE_METHOD = "DELETE"

    # --------------------SUPPORT ROLE NAME ------------------
    SUPPORT_ROLE_NAME = "SUPPORT"

    # ------------- Authentication APP --------------------

    CUSTOM_USER = "custom_user"
    USER_PROFILE = "user_profile"
    CUSTOM_PERMISSION = "custom_permission"
    PERMISSION_CATEGORY = "permission_category"
    ROLES = "roles"
    ROLE_NAME = "SUPPORT"
    USER_PERMISSION_CACHE_KEY = "user_permissions_cache"
    COURSE = "course"

    # --------------------------------------------------------API LOGS--------------------------
    # API_LOGS = "api_logs"

    # ---------------------------All Model List -For Management Command-----------------
    ALL_MODELS_LIST = {
        "CUSTOM_USER": CUSTOM_USER,
        "USER_PROFILE": USER_PROFILE,
        "CUSTOM_PERMISSION": CUSTOM_PERMISSION,
        "PERMISSION_CATEGORY": PERMISSION_CATEGORY,
        "ROLES": ROLES,
        "COURSE": COURSE,
        # "API_LOGS": API_LOGS,
    }


class HttpBasedPermissionActionMaps:
    CAN_CREATE = "can_create"
    CAN_VIEW = "can_view"
    CAN_UPDATE = "can_update"
    CAN_DELETE = "can_delete"
