from django.conf import settings
from django.contrib import admin
from django.urls import path, include


# Admin path is intentionally configurable for security reasons
urlpatterns = [
    path(settings.ADMIN_PATH, admin.site.urls),
    path('',include('final.urls'))
]
