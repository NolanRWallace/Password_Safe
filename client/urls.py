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
    path('new/data', views.new_data),
    path('new/email', views.new_email),
    path('new/password', views.new_password),
    path('new/combo', views.new_combo,),
    path('proccess/combo', views.add_combo), 
    path('combo/edit/<int:combo_id>', views.edit_combo),
    path('combo/delete/<int:combo_id>', views.delete_combo),
    path('proccess/combo/edit/<int:combo_id>', views.proccess_edit_combo)
]