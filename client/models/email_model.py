from django.db import models
import re
from django.contrib import messages
from .user_model import User

class EmailManager(models.Manager):
    def email_validation(self, form_data, session_id):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(form_data['email']):
            errors['email'] = "Must be a valid email address"
        current_user = User.objects.get(id = session_id)
        all_emails = Emails.objects.filter(user = current_user)
        for email in all_emails:
            if email.email == form_data['email']:
                errors['email'] = "Email already in use"
        if form_data['email'] != form_data['confirm_email']:
            errors['confirm_email'] = "Emails do not match, check and resubmit"
        return errors
    
    def email_edit_validation(self, form_data, session_id, email_id):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(form_data['email']):
            errors['email'] = "Must be a valid email address"
        current_user = User.objects.get(id = session_id)
        all_emails = Emails.objects.filter(user = current_user).exclude(id=email_id)
        for email in all_emails:
            if email.email == form_data['email']:
                errors['email'] = "Email already in use"
        if form_data['email'] != form_data['confirm_email']:
            errors['confirm_email'] = "Emails do not match, check and resubmit"
        return errors
        
    
class Emails(models.Model):
    email = models.EmailField()
    user = models.ForeignKey(User, related_name='emails', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = EmailManager()