from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import URL


class UserForm(UserCreationForm):


    class Meta:


       model = User
       fields = ['username', 'email', 'password1', 'password2']


class URLForm(forms.ModelForm):


    class Meta:


        model = URL
        fields = ['url', 'short', 'description' ]
