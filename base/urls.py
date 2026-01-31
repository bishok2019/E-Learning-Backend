from django.urls import include, path

urlpatterns = [
    path("v1/", include("base.api_urls.v1.urls")),
    # path("v2/", include("apps.base.api_urls.v2.urls")),
]
