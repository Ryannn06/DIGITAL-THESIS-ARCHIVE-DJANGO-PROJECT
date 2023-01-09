from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from libraryApp.models import Registrations, ColCourse
from django.core.exceptions import ValidationError
import re

class RegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email Address','required':'required',}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First Name','required':'required',}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name','required':'required',}))
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username','required':'required',}))
    
    error_messages = {
            'username': {
                'unique': ("Username already exists"),
            },
        }

    class Meta:
        model = Registrations
        fields = ['username','first_name','last_name','email','password1','password2']

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        # Making location required
        self.fields['email'].help_text = "Use only valid TUP Cavite gsfe account"

    def clean_email(self):
        pattern_with_email = "[a-z,-_,]@[g][s][f][e].[t][u][p][c][a][v][i][t][e].[e][d][u].[p][h]"
        data_2 = self.cleaned_data['email'] 

        if not re.search(pattern_with_email, data_2):
            raise ValidationError("Please enter valid Tup-Cavite gsfe account")
        return data_2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_student= True
        if commit:
            user.save()
        return user


class RegisterStaffForm(UserCreationForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email Address','required':'required',}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First Name','required':'required',}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name','required':'required',}))
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username','required':'required',}))

    class Meta:
        model = Registrations

        fields = ['username','first_name','last_name','email','password1','password2']
 
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff= True
        user.is_admin = True
        if commit:
            user.save()
        return user


