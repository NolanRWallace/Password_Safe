from django.urls import path     
from ..views import reg_login_views


urlpatterns = [
    path('', reg_login_views.index),
    path('login', reg_login_views.login_form),
    path('login/process', reg_login_views.login),
    path('registration', reg_login_views.reg_form),
    path('register', reg_login_views.reg),
    path('home', reg_login_views.home),
    path('logout', reg_login_views.logout),
]