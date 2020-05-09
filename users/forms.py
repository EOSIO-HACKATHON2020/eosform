from django import forms
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from django.contrib.auth.forms import UsernameField
from .models import User


class UserCreationForm(BaseUserCreationForm):

    class Meta:
        model = User
        fields = ("email",)
        field_classes = {'email': UsernameField}
