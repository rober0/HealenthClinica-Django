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
        fields = ['username', 'email', 'cpf', 'data_nascimento', 'numero', 'genero']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'email': forms.EmailInput(attrs={'class': 'form-control form-control-lg'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'data_nascimento': forms.DateInput(attrs={
                'class': 'form-control form-control-lg',
                'type': 'date'
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