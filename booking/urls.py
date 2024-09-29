from django.urls import path
from .views import booking_history, make_booking

urlpatterns = [
    path('history/', booking_history, name='booking_history'),
    path('new/', make_booking, name='make_booking'),
]
