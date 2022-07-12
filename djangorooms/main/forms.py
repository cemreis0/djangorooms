from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Room, User
from django.core.exceptions import ValidationError
from django import forms
from django.forms.forms import Form

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = ['topic', 'name', 'description']


class RegisterForm(UserCreationForm):
    username = forms.CharField(label='username', min_length=3, max_length=150)  
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)  
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)  

    def username_clean(self):  
        username = self.cleaned_data['username'].lower()  
        new = User.objects.filter(username = username)  
        if new.count():  
            raise ValidationError("Kullanıcı mevcut.")  
        return username  
  
    def clean_password2(self):  
        password1 = self.cleaned_data['password1']  
        password2 = self.cleaned_data['password2']  
  
        if password1 and password2 and password1 != password2:  
            raise ValidationError("Şifreler uyumsuz.")  
        return password2  
  
    def save(self, commit=True):  
        user = User.objects.create_user(  
            self.cleaned_data['username'],
            self.cleaned_data['password1']  
        )  
        return user  