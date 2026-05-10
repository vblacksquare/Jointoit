
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("Core.urls"), name="core"),
    path('api/v1/users/', include("Users.urls"), name="users"),
    path('api/v1/', include("Events.urls"), name="event"),
]
