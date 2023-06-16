from django import forms
from django.contrib import admin

from .models import OTP, User


# Register your models here.

class UserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'


class UserAdmin(admin.ModelAdmin):
    form = UserAdminForm


admin.site.register(User, UserAdmin)
admin.site.register(OTP)
