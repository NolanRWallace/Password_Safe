from django.urls import path     
from ..views import reg_login_views


urlpatterns = [
    path('', reg_login_views.index),
    path('login', reg_login_views.login_form, name='login'),
    path('login/process', reg_login_views.login, name='process_login'),
    path('registration', reg_login_views.reg_form, name='registration'),
    path('register', reg_login_views.reg, name='process_reg'),
    path('home', reg_login_views.home, name='home'),
    path('logout', reg_login_views.logout, name='logout'),
]