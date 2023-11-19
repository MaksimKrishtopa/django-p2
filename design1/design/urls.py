from django.conf import settings
from django.contrib import admin
from django.template.context_processors import static
from django.urls import path, include
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('superadmin', admin.site.urls),
    path('', include('catalog.urls')),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)