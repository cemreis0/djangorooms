from pyexpat import model
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Room, User
from django.core.exceptions import ValidationError
from django import forms
from django.forms.forms import Form

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'description', 'topic']
        exclude = ['host', 'participants']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': "form-control"}),
            }


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    
class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']