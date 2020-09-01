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
    path('new/entry', views.new_entry),
    
]