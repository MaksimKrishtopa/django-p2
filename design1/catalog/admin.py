from django.contrib import admin
from .models import DesignRequest, DesignCategory

admin.site.register(DesignRequest)
admin.site.register(DesignCategory)