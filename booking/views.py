from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Booking

@login_required
def booking_history(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'booking/booking_history.html', {'bookings': bookings})

@login_required
def make_booking(request):
    if request.method == 'POST':
        # Handle booking logic here
        pass

    return render(request, 'booking/make_booking.html')
