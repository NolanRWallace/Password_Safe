from django.urls import path     
from ..views import password_views


urlpatterns = [
    path('add/password', password_views.add_password),
    path('new/password', password_views.new_password),
    path('password/delete/<int:pass_id>', password_views.delete_password),
    path('edit/password/<int:pass_id>', password_views.edit_password),
    path('process/edit/password/<int:pass_id>', password_views.process_edit_password),
]