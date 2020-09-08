from django.urls import path     
from . import views
from .models import User

urlpatterns = [
    path('', views.index),
    path('login', views.login_form),
    path('login/process', views.login),
    path('registration', views.reg_form),
    path('register', views.reg),
    path('home', views.home),
    path('add/email', views.add_email),
    path('new/email', views.new_email),
    path('add/password', views.add_password),
    path('new/password', views.new_password),
    path('new/combo', views.new_combo,),
    path('proccess/combo', views.add_combo), 
    path('combo/edit/<int:combo_id>', views.edit_combo),
    path('combo/delete/<int:combo_id>', views.delete_combo),
    path('proccess/combo/edit/<int:combo_id>', views.proccess_edit_combo),
    path('logout', views.logout),
    path('email/delete/<int:email_id>', views.delete_email),
    path('password/delete/<int:pass_id>', views.delete_password),
    path('edit/email/<int:email_id>', views.edit_email),
    path('process/edit/email/<int:email_id>', views.process_edit_email),
    path('edit/password/<int:pass_id>', views.edit_password),
    path('process/edit/password/<int:pass_id>', views.process_edit_password),
]