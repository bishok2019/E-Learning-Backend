from django.urls import include, path

from .views import (
    ChangeUserPasswordView,
    LoginView,
    LogoutView,
    PermissionsCategoryListView,
    PermissionsListDropdownView,
    PermissionsListView,
    RefreshTokenView,
    RolesCreateView,
    RolesListDropdownView,
    RolesListView,
    RolesRetrieveView,
    RolesUpdateView,
    UserCreateView,
    UserListView,
    UserRetrieveView,
    UserUpdateView,
    CustomUserSignUpAPIView,
)

roles_and_permissions_patterns = [
    path(
        "permissions/categories/list",
        PermissionsCategoryListView.as_view(),
        name="permissions-category-list",
    ),
    path("permissions/list", PermissionsListView.as_view(), name="permissions-list"),
    path(
        "permissions/dropdown",
        PermissionsListDropdownView.as_view(),
        name="permissions-list-dropdown",
    ),
    path("roles/list", RolesListView.as_view(), name="roles-list"),
    path(
        "roles/dropdown", RolesListDropdownView.as_view(), name="roles-list-dropdown"
    ),
    path("roles/create", RolesCreateView.as_view(), name="roles-create"),
    path("roles/retrieve/<int:pk>", RolesRetrieveView.as_view(), name="roles-retrieve"),
    path("roles/update/<int:pk>", RolesUpdateView.as_view(), name="roles-update"),
]
authentication_patterns = [
    path("login", LoginView.as_view(), name="login"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("token/refresh", RefreshTokenView.as_view(), name="token-refresh"),
    path("users", UserListView.as_view(), name="user-list"),
    path("users/create", UserCreateView.as_view(), name="user-create"),
    path("users/retrieve/<int:pk>", UserRetrieveView.as_view(), name="user-retrieve"),
    path("users/update/<int:pk>", UserUpdateView.as_view(), name="user-update"),
    path(
        "users/change-password/<int:pk>",
        ChangeUserPasswordView.as_view(),
        name="change-user-password",
    ),
    path("signup", CustomUserSignUpAPIView.as_view(), name="user-signup"),
    path("", include(roles_and_permissions_patterns)),
]
urlpatterns = authentication_patterns
