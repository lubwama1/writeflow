from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

from django import forms


class EmailChangeForm(forms.Form):
    new_email = forms.EmailField(
        label="New Email",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your new email'
        })
    )

    def __init__(self, *args, **kwargs):
        super(EmailChangeForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label_suffix = ''
            if field.label and '*' in field.label:
                field.label = field.label.replace('*', '')


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.TextInput(  
        attrs={'class': 'email-class', 'placeholder': 'rayntukea@gmail.com'}))
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'eg. jon doe'}))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', id: 'password'}), label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control'}), label='Password Confirmation')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProfileForm(forms.ModelForm):
    birth_date = forms.CharField(
        widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Profile
        fields = [
            'first_name', 'last_name', 'birth_date', 'gender', 'image'
        ]

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label_suffix = ''
            if field.label and '*' in field.label:
                field.label = field.label.replace('*', '')

class CustomLoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'checkbox'}))
    def clean_username(self):
        username = self.cleaned_data['username']
        if not username:
            raise forms.ValidationError("Username is required")
        return username
    def clean_password(self):
        password = self.cleaned_data['password']
        if not password:
            raise forms.ValidationError("Password is required")
        return password