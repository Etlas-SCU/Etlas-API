from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.core.files.storage import default_storage
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from rest_framework_simplejwt.tokens import RefreshToken

# Create your models here.


class UserManager(BaseUserManager):
    
    def create_user(self, email, full_name, address=None, phone_number=None, image=None, password=None):
        if full_name is None:
            raise TypeError('Users must have a full name')
        
        if email is None:
            raise TypeError('Users must have an email address')
            
        user = self.model(email=self.normalize_email(email), full_name=full_name, address = address, phone_number = phone_number, image=image)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, full_name, password=None):
        if password is None:
            raise TypeError('Password should not be none')
        
        user = self.create_user(email = email, full_name = full_name, password = password)
        user.is_superuser = True
        user.is_staff = True
        user.is_verified = True
        user.save()
        return user


AUTH_PROVIDERS = {'facebook': 'facebook', 'google': 'google', 'twitter': 'twitter', 'email': 'email'}


class User(AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    best_score = models.IntegerField(default=0)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    auth_provider = models.CharField(max_length=255, blank=False, null=False, default=AUTH_PROVIDERS.get('email'))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    objects = UserManager()

    def __str__(self):
        return self.email
    
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    
    def delete(self, *args, **kwargs):
        # Delete the image file from Backblaze B2 bucket
        default_storage.delete(self.image.name)
        super().delete(*args, **kwargs)


@receiver(pre_delete, sender=User)
def delete_image(sender, instance, **kwargs):
    """
    Delete the image file from Backblaze B2 bucket when the instance of the model
    is deleted.
    """
    default_storage.delete(instance.image.name)


class OTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=4)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.otp
    