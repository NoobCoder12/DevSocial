from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': "mb-3 row", 'placeholder': 'Create username'}),
            'email': forms.TextInput(attrs={'class': "mb-3 row", 'placeholder': 'Provide email'}),
            'password1': forms.PasswordInput(attrs={'class': "mb-3 row", 'placeholder': 'Create password'}),
            'password2': forms.PasswordInput(attrs={'class': "mb-3 row", 'placeholder': 'Confirm password'}),
        }

        def clean_email(self):
            email = self.cleaned_data.get('email')
            if User.objects.filter(email='email').exists():
                raise forms.ValidationError('This email is already in use')
            return email
