from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from booking.models import Booking
from .forms import ProfileForm, CustomPasswordChangeForm, PreferencesForm
from.decorators import role_required
from django.contrib import messages


@login_required
def dashboard(request):
    profile = request.user
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'user/dashboard.html', {'profile': profile, 'bookings': bookings})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ProfileForm(instance=request.user)

    return render(request, 'user/edit_profile.html', {'form': form})


@role_required(allowed_roles=['admin', 'staff'])
def admin_dashboard(request):
    return render(request, 'admin/dashboard.html')


@role_required(allowed_roles=['admin', 'staff'])
def staff_dashboard(request):
    return render(request, 'staff/dashboard.html')


@role_required(allowed_roles='provider')
def provider_dashboard(request):
    return render(request, 'provider/dashboard.html')


@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep user logged in after password change
            messages.success(request, 'Your password was successfully updated!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'user/change_password.html', {'form': form})


@login_required
def manage_preferences(request):
    if request.method == 'POST':
        form = PreferencesForm(request.POST)
        if form.is_valid():
            form.save(request.user)  # Save preferences to the user model
            messages.success(request, 'Your preferences have been updated successfully!')
            return redirect('dashboard')
    else:
        # Initialize the form with current preferences
        initial_data = {
            'email_notifications': request.user.preferences.get('email_notifications', False),
            'sms_notifications': request.user.preferences.get('sms_notifications', False),
            'language': request.user.preferences.get('language', 'en'),
        }
        form = PreferencesForm(initial=initial_data)

    return render(request, 'user/manage_preferences.html', {'form': form})