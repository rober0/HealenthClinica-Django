from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

class RegistroForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control form-control-lg'})
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg'})
    )
    
    def __init__(self, *args, **kwargs):
        super(RegistroForm, self).__init__(*args, **kwargs)
        del self.fields['password2']

    class Meta:
        model = User
        fields = ['username', 'email', 'password1']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Este email já está em uso")
        return email

class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control form-control-lg',
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
        })
    )

    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if email and password:
            try:
                user = User.objects.get(email=email)
                self.user_cache = authenticate(
                    username=user.username,
                    password=password
                )
                if self.user_cache is None:
                    raise forms.ValidationError('Email ou senha inválidos.')
                
            except User.DoesNotExist:
                raise forms.ValidationError('Email ou senha inválidos.')

        return self.cleaned_data