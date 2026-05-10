
from django.urls import path
from .views import (
    SpectacularView,
    SwaggerView,
    RedocView,
)

urlpatterns = [
    path("api/schema/", SpectacularView.as_view(), name="schema"),
    path("api/docs/", SwaggerView.as_view(url_name="schema")),
    path("api/redoc/", RedocView.as_view(url_name="schema")),
]
