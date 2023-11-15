from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone  # Импорт пространства имен для timezone

class DesignRequest(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]

    title = models.CharField(max_length=255, default='Title')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)  # Убедитесь, что у вас есть этот импорт
    category = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='design_photos/', default='design_photos/default.jpg')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return self.title
class RequestCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name