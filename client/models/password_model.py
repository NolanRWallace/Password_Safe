from django.db import models
from .user_model import User

class Passwords(models.Model):
    password = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name='passwords', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)