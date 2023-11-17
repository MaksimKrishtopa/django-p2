from django.db import models
from django.contrib.auth.models import User
from django.db import models

from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fio = models.CharField(max_length=255, blank=False, verbose_name=_('ФИО'))

    def __str__(self):
        return self.user.username


class DesignRequest(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey("DesignCategory", max_length=150, verbose_name='designrequest category', blank=False,
                                 on_delete=models.CASCADE)

    description = models.TextField()
    image = models.ImageField(upload_to='design_images/', blank=True, null=True)
    photo = models.ImageField(upload_to='design_photos/', default='no-photo.jpg')

    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь", default=None)
    status = models.CharField(max_length=20, choices=[('Новая', 'Новая'), ('Принято в работу', 'Принято в работу'),
                                                      ('Выполнено', 'Выполнено')], default='Новая')

    def __str__(self):
        return self.title


class DesignCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Название категории'))

    def __str__(self):
        return self.name
