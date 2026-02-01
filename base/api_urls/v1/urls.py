from django.urls import include, path

urlpatterns = [
    path("auth_app/", include("apps.authentication.urls")),
    path("course_app/", include("apps.course.urls")),
]
