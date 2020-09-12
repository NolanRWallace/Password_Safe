from django.urls import path     
from ..views import  email_views 


urlpatterns = [
    path('add/email', email_views.add_email),
    path('new/email', email_views.new_email),
    path('email/delete/<int:email_id>', email_views.delete_email),
    path('edit/email/<int:email_id>', email_views.edit_email),
    path('process/edit/email/<int:email_id>', email_views.process_edit_email),
]