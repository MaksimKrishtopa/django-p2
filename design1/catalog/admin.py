# admin.py

from django import forms
from django.contrib import admin

from .forms import ChangeStatusForm
from .models import DesignRequest, DesignCategory




admin.site.register(DesignCategory)
@admin.register(DesignRequest)
class DesignRequestn(admin.ModelAdmin):
    form = ChangeStatusForm
    list_display = ("title", "category")