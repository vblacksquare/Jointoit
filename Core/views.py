
from rest_framework.permissions import IsAdminUser

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)


class SpectacularView(SpectacularAPIView):
    permission_classes = [IsAdminUser]


class SwaggerView(SpectacularSwaggerView):
    permission_classes = [IsAdminUser]


class RedocView(SpectacularRedocView):
    permission_classes = [IsAdminUser]
