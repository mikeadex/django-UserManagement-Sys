from django import forms
from .models import CustomUser
from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth.forms import PasswordChangeForm


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')
    phone_number = forms.CharField(max_length=15, label='Phone Number', required=False)

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone_number = self.cleaned_data['phone_number']
        user.save()
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'phone_number', 'address', 'profile_picture', 'company_name',
                  'bio', 'location']


class CustomPasswordChangeForm(PasswordChangeForm):
    pass


class PreferencesForm(forms.Form):
    email_notifications = forms.BooleanField(required=False, label='Email Notifications')
    sms_notifications = forms.BooleanField(required=False, label='SMS Notifications')
    language = forms.ChoiceField(choices=[('en', 'English'), ('fr', 'French')], label='Preferred Language')

    def save(self, user):
        # Convert form data into a dictionary and store it as JSON in the user model
        preferences = {
            'email_notifications': self.cleaned_data['email_notifications'],
            'sms_notifications': self.cleaned_data['sms_notifications'],
            'language': self.cleaned_data['language'],
        }
        user.preferences = preferences
        user.save()
