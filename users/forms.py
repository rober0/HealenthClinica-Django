from django import forms
from .models import Paciente

class RegistroForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control form-control-lg'
    }))
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control form-control-lg'
    }))

    class Meta:
        model = Paciente
        fields = ['username', 'email', 'data_nascimento', 'numero', 'genero']
        widgets = {
            'username': forms.TextInput(attrs={'type': 'text', 'class': "input validator", 'name': 'username', 'required placeholder': 'Nome', 'minlength': '3', 'pattern': '[A-Za-zÀ-ÖØ-öø-ÿ\s]{3,}', 'title': 'Must be more than 3 characters, only letters and spaces'
                                               }),
            'email': forms.EmailInput(attrs={'type': 'email', 'class': "input validator", 'placeholder': '@', 'required': 'required'}),
            'data_nascimento': forms.DateInput(attrs={
                'type': "date", 'class': "input validator", 'required placeholder': "Pick a date in 2025", 'min': "1935-01-01", 'max': "2025-12-31", 'title': "Must be valid"
            }),
            'numero': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'genero': forms.Select(attrs={
                'class': 'form-control form-control-lg'
            }, choices=[
                ('', 'Selecione o gênero'),
                ('M', 'Masculino'),
                ('F', 'Feminino'),
                ('O', 'Outro')
            ]),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm:
            if password != password_confirm:
                raise forms.ValidationError("As senhas não coincidem")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control form-control-lg'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control form-control-lg'
    }))