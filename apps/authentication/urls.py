from django.urls import include, path

from .views import (
    ChangeUserPasswordView,
    CustomUserSignUpAPIView,
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
)

permissions_patterns = [
    path(
        "categories/list",
        PermissionsCategoryListView.as_view(),
        name="permissions-category-list",
    ),
    path("list", PermissionsListView.as_view(), name="permissions-list"),
    path(
        "dropdown",
        PermissionsListDropdownView.as_view(),
        name="permissions-list-dropdown",
    ),
]
roles_patterns = [
    path("list", RolesListView.as_view(), name="roles-list"),
    path("dropdown", RolesListDropdownView.as_view(), name="roles-list-dropdown"),
    path("create", RolesCreateView.as_view(), name="roles-create"),
    path("retrieve/<int:pk>", RolesRetrieveView.as_view(), name="roles-retrieve"),
    path("update/<int:pk>", RolesUpdateView.as_view(), name="roles-update"),
]

user_patterns = [
    path("list", UserListView.as_view(), name="user-list"),
    path("create", UserCreateView.as_view(), name="user-create"),
    path("retrieve/<int:pk>", UserRetrieveView.as_view(), name="user-retrieve"),
    path("update/<int:pk>", UserUpdateView.as_view(), name="user-update"),
    path(
        "change-password/<int:pk>",
        ChangeUserPasswordView.as_view(),
        name="change-user-password",
    ),
]
authentication_patterns = [
    path("login", LoginView.as_view(), name="login"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("refresh-token", RefreshTokenView.as_view(), name="token-refresh"),
    path("signup", CustomUserSignUpAPIView.as_view(), name="user-signup"),
    path("users/", include(user_patterns)),
    path("permissions/", include(permissions_patterns)),
    path("roles/", include(roles_patterns)),
]
urlpatterns = authentication_patterns
