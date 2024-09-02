from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, unique=True)
    priority = models.CharField(max_length=10, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')])
    description = models.TextField()
    admin = models.ForeignKey(User, related_name='tasks_admin', on_delete=models.CASCADE)
    teacher = models.ForeignKey(User, related_name='tasks_teacher', on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
