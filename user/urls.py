from django.urls import path
from .views import (dashboard, edit_profile, admin_dashboard, staff_dashboard, provider_dashboard, change_password,
                    manage_preferences)

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('edit-profile/', edit_profile, name='edit_profile'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('staff-dashboard/', staff_dashboard, name='staff_dashboard'),
    path('provider-dashboard/', provider_dashboard, name='provider_dashboard'),
    path('change-password/', change_password, name='change_password'),
    path('manage-preferences/', manage_preferences, name='manage_preferences'),


]
