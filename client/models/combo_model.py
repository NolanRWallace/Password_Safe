from django.db import models
from .user_model import User
from .password_model import Passwords
from .email_model import Emails

class ComboManager(models.Manager):
    def combo_validation(self, form_data, session_id):
        errors = {}
        current_user = User.objects.get(id=session_id)
        all_combos = Combo.objects.filter(user = current_user)
        if len(form_data['accountName']) < 2:
            errors["accountName"] = "Account Name must be at least 2 characters long"
        for combo in all_combos:
            if combo.accountName.lower() == form_data['accountName'].lower():
                errors['unique'] = "Account Name already in Use"
        if form_data['email'] == "None":
            errors['email'] = "Please Select an Email"
        if form_data['password'] == "None":
            errors['password'] = "Please Select a Password"
        return errors
            
        
    
class Combo(models.Model):
    accountName = models.CharField(max_length=50)
    email = models.ForeignKey(Emails, related_name='combos', on_delete=models.CASCADE)
    password = models.ForeignKey(Passwords, related_name="combos", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='combos', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now = True)
    objects = ComboManager()
