from django.contrib import admin

# Register your models here.
# catalog/admin.py
from .models import DesignRequest, UserProfile

admin.site.register(DesignRequest)
admin.site.register(UserProfile)