from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django_password_eye.fields import PasswordEye
from .models import Profile

class UserLoginForm(forms.Form):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))  # Hidden password field



class UserSignupForm(UserCreationForm):
    email = forms.EmailField(
        label='Email',
        max_length=254,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    username = forms.CharField(
        label='Username',
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    user_type = forms.ChoiceField(
        choices=[('', '---------'), ('buyer', 'Buyer'), ('seller', 'Seller')],
        label='I am a',
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'user_type'})
    )
    gst_number = forms.CharField(
        label='GST Number',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'gst_number'})
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'user_type', 'gst_number')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            profile = Profile.objects.get(user=user)
            profile.user_type = self.cleaned_data['user_type']
            profile.gst_number = self.cleaned_data['gst_number']
            profile.save()
        return user