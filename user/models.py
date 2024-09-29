from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.conf import settings
import os


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault(('is_staff'), True)
        extra_fields.setdefault(('is_superuser'), True)

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ('client', 'Client'),
        ('provider', 'Service Provider'),

    )
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    preferences = models.JSONField(default=dict, blank=True)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='client')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        try:
            # Get the old profile image before saving the new one
            old_profile = CustomUser.objects.get(pk=self.pk)
            old_image = old_profile.profile_picture
        except CustomUser.DoesNotExist:
            old_image = None

        # Call the original save() method to save the new image
        super(CustomUser, self).save(*args, **kwargs)

        # If there's an old image and it's different from the new one, delete the old image
        if old_image and old_image != self.profile_picture:
            if os.path.isfile(os.path.join(settings.MEDIA_ROOT, old_image.path)):
                os.remove(os.path.join(settings.MEDIA_ROOT, old_image.path))

    def __str__(self):
        return self.email
