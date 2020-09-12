from django.db import models
import re
from django.contrib import messages
from .user_model import User

class EmailManager(models.Manager):
    def email_validation(self, form_data):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(form_data['email']):
            errors['email'] = "Must be a valid email address"
        all_emails = Emails.objects.all()
        for email in all_emails:
            if email.email == form_data['email']:
                errors['email'] = "Email already in use"
        return errors
        
    
class Emails(models.Model):
    email = models.EmailField()
    user = models.ForeignKey(User, related_name='emails', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = EmailManager()