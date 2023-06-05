from django.contrib import admin
from django.urls import path, include
import public_libraries

urlpatterns = [
    path("db/", admin.site.urls),
    path("", include("public_libraries.urls")),
    path("api/v1/", include("api.urls")),
]
