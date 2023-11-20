# admin.py

from django import forms
from django.contrib import admin
from .models import DesignRequest, DesignCategory

class DesignRequestAdminForm(forms.ModelForm):
    class Meta:
        model = DesignRequest
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        photo = cleaned_data.get('photo')

        if status == 'Выполнено' and not photo:
            raise forms.ValidationError({'photo': 'Добавьте изображение дизайна для статуса "Выполнено".'})

        comment = cleaned_data.get('comment')
        if status == 'Принято в работу' and not comment:
            raise forms.ValidationError({'comment': 'Добавьте комментарий для статуса "Принято в работу".'})

class DesignRequestAdmin(admin.ModelAdmin):
    form = DesignRequestAdminForm
    list_display = ('title', 'category', 'status', 'user', 'timestamp')
    actions = ['mark_as_in_progress', 'mark_as_completed']

    def mark_as_in_progress(modeladmin, request, queryset):
        for design_request in queryset:
            if design_request.status == 'Новая':
                design_request.status = 'Принято в работу'
                design_request.save()

    mark_as_in_progress.short_description = "Отметить как 'Принято в работу'"

    def mark_as_completed(modeladmin, request, queryset):
        for design_request in queryset:
            if design_request.status == 'Новая':
                design_request.status = 'Выполнено'
                design_request.save()

    mark_as_completed.short_description = "Отметить как 'Выполнено'"

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj and obj.status == 'Принято в работу':
            form.base_fields['comment'].required = True
        elif obj and obj.status == 'Выполнено':
            form.base_fields['photo'].required = True
        return form

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        if obj and obj.status in ('Принято в работу', 'Выполнено'):
            readonly_fields += ('status',)
        return readonly_fields

    def save_model(self, request, obj, form, change):
        if obj.status == 'Выполнено' and not obj.photo:
            raise forms.ValidationError({'photo': 'Добавьте изображение дизайна для статуса "Выполнено".'})
        elif obj.status == 'Выполнено':
            obj.comment = ""  # Сбрасываем комментарий, если статус "Выполнено"
        elif obj.status == 'Принято в работу':
            obj.photo = None  # Сбрасываем изображение, если статус "Принято в работу"
        obj.save()

admin.site.register(DesignRequest, DesignRequestAdmin)
admin.site.register(DesignCategory)
