from django.db import models
from .user_model import User

class PasswordManager(models.Manager):
    def password_validation(self, form_password, confirm_pw, session_id):
        errors = {}
        current_user = User.objects.get(id=session_id)
        all_passwords = Passwords.objects.filter(user = current_user)
        for password in all_passwords:
            if password.password == form_password:
                errors['unique'] = "Password already Exists"
        if len(form_password) < 2:
            errors['password'] = "Password must be at least 2 characters in length"
        if form_password != confirm_pw:
            errors['confirm_pw'] = "Passwords Do Not Match. Try Again"
        return errors
    
    def password_edit_validation(self, pass_id, form_password, confirm_pw, session_id):
        errors = {}
        current_user = User.objects.get(id=session_id)
        all_passwords = Passwords.objects.filter(user = current_user).exclude(id=pass_id)
        for password in all_passwords:
            if password.password == form_password:
                errors['unique'] = "Password already Exists"
        if len(form_password) < 2:
            errors['password'] = "Password must be at least 2 characters in length"
        if form_password != confirm_pw:
            errors['confirm_pw'] = "Passwords Do Not Match. Try Again"
        return errors

class Passwords(models.Model):
    password = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name='passwords', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = PasswordManager()