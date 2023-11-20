# models.py
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.db.models.signals import pre_save

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fio = models.CharField(max_length=255, blank=False, verbose_name=_('ФИО'))

    def __str__(self):
        return self.user.username


from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class DesignCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Название категории'))

    def __str__(self):
        return self.name


@receiver(pre_delete, sender=DesignCategory)
def delete_requests_with_category(sender, instance, **kwargs):
    DesignRequest.objects.filter(category=instance).delete()


class DesignRequest(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey("DesignCategory", max_length=150, verbose_name='designrequest category', blank=False, on_delete=models.CASCADE)
    description = models.TextField()
    photo = models.ImageField(upload_to='design_photos/', blank=False, null=True, validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg', 'bmp'])])
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь", default=None)
    status = models.CharField(max_length=20, choices=[('Новая', 'Новая'), ('Принято в работу', 'Принято в работу'), ('Выполнено', 'Выполнено')], default='Новая')
    comment = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.status == 'Выполнено' and not self.photo:
            raise ValidationError({'photo': 'Добавьте изображение дизайна для статуса "Выполнено".'})
        elif self.status == 'Выполнено':
            self.comment = ""  # Сбрасываем комментарий, если статус "Выполнено"
        elif self.status == 'Принято в работу':
            self.photo = None  # Сбрасываем изображение, если статус "Принято в работу"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title