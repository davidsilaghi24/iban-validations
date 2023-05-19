from django.contrib import admin
from validations.views import CustomAuthToken
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/",
        include(("validations.urls", "validations"),
                namespace="validations")
    ),
    # drf-spectacular endpoints
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui"
    ),
    path("api-token-auth/", CustomAuthToken.as_view(), name="api_token_auth"),
]
