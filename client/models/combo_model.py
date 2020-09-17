from django.db import models
from .user_model import User
from .password_model import Passwords
from .email_model import Emails

# class ComboManager(models.Manager):
#     def combo_validation(self, form_data):
#         error = {}
        
    
class Combo(models.Model):
    accountName = models.CharField(max_length=50)
    email = models.ForeignKey(Emails, related_name='combos', on_delete=models.CASCADE)
    password = models.ForeignKey(Passwords, related_name="combos", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='combos', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now = True)
