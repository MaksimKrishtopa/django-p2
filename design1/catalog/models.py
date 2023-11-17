
from django.db import models
from django.contrib.auth.models import User
from django.db import models

from django.utils.translation import gettext_lazy as _

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fio = models.CharField(max_length=255, blank=False, verbose_name=_('ФИО'))

    def __str__(self):
        return self.user.username

class DesignRequest(models.Model):
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='design_images/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('In Progress', 'In Progress'), ('Completed', 'Completed')])

    def __str__(self):
        return self.title
