from django.db import models
import re, bcrypt
from django.contrib import messages

# Create your models here.
class UserManager(models.Manager):
    def reg_validation(self, form_data):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(form_data['f_name']) < 2:
            errors['f_name'] = "First Name Must be at least 2 characters long"
        if len(form_data['l_name']) < 2:
            errors['l_name'] = "Last Name must be at least 2 characters long"
        if not EMAIL_REGEX.match(form_data['email']):
            errors['email'] = "Must be a valid email address"
        if len(form_data['password']) < 8:
            errors['password'] = "Password has to be at least 8 characters"
        if form_data['password'] != form_data['confirm_pw']:
            errors['confirm_pw'] = "Passwords must match each other"
        return errors
            
    def login_validation(self, user_data):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(user_data['email']):
            errors['email'] = "Must be a valid email address"
        if len(user_data['password']) < 8:
            errors['password'] = "Password has to be at least 8 characters"
            
        return errors
    
class User(models.Model):
    f_name = models.CharField(max_length=50)
    l_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = UserManager()
    
class EmailManager(models.Manager):
    def email_validation(self, form_data):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(form_data['email']):
            errors['email'] = "Must be a valid email address"
        return errors
        
    
class Emails(models.Model):
    email = models.EmailField(unique=True)
    user = models.ForeignKey(User, related_name='emails', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = EmailManager()
    
    
class Passwords(models.Model):
    password = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name='passwords', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    
# class ComboManager(models.Manager):
#     def reg_validation(self, form_data):
#         errors = {}
#         EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
#         if len(form_data['accountName']) < 2:
#             errors['accountName'] = "Account name cannot be less than 2 characters in length"
#         if not EMAIL_REGEX.match(form_data['email']):
#             errors['email'] = "Must be a valid email address"
#         if len(form_data['password']) < 8:
#             errors['password'] = "Password has to be at least 8 characters"
#         if form_data('password') != form_data('confirm_pw'):
#             errors['confirm_pw'] = "Passwords must match each other"
#         return errors
    
class Combo(models.Model):
    accountName = models.CharField(max_length=50)
    email = models.ForeignKey(Emails, related_name='combos', on_delete=models.CASCADE)
    password = models.ForeignKey(Passwords, related_name="combos", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='combos', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now = True)
    # objects = ComboManager()
    
