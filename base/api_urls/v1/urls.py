from django.urls import include, path

urlpatterns = [
    path("auth_app/", include("apps.authentication.urls")),
]
