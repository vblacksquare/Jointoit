
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (EventViewSet)


event_router = DefaultRouter()
event_router.register(r"events", EventViewSet, basename="events")


urlpatterns = [
    path("", include(event_router.urls)),
]
