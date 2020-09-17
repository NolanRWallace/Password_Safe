from django.urls import path     
from ..views import combo_views

urlpatterns = [
    path('new/combo', combo_views.new_combo, name='add_combo'),
    path('proccess/combo', combo_views.add_combo, name='new_combo'), 
    path('combo/delete/<int:combo_id>', combo_views.delete_combo, name='delete_combo'),
    path('combo/edit/<int:combo_id>', combo_views.edit_combo, name='edit_combo'),
    path('proccess/combo/edit/<int:combo_id>', combo_views.proccess_edit_combo, name='process_edit_combo'),
]