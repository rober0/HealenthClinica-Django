from django import forms
from .models import Paciente

class RegistroForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'type': "password", 'required placeholder': "Senha", 'minlength': "8", 'title': "Must be more than 8 characters, including number, lowercase letter, uppercase letter"
    }))
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={
        'type': "password", 'required placeholder': "Confirme a Senha", 'minlength': "8", 'title': "Must be more than 8 characters, including number, lowercase letter, uppercase letter"
    }))

    class Meta:
        model = Paciente
        fields = ['username', 'email', 'data_nascimento', 'telefone', 'genero']
        widgets = {
            'username': forms.TextInput(attrs={'type': 'text', 'class': "input validator", 'name': 'username', 'required placeholder': 'Nome', 'minlength': '3', 'title': 'Must be more than 3 characters, only letters and spaces'
                                               }),
            'email': forms.EmailInput(attrs={'type': 'email', 'class': "input validator", 'placeholder': 'exemplo@gmail.com', 'required': 'required'}),
            'data_nascimento': forms.DateInput(attrs={
                'type': "date", 'class': "input validator", 'min': "1935-01-01", 'max': "2025-12-31", 'title': "Must be valid"
            }),
            'telefone': forms.TextInput(attrs={'type': "tel", "id": "phone", 'placeholder': "Telefone", 'class': "input validator", 'required': "required"}),
            'genero': forms.Select(attrs={
                'class': "select validator", 'required': "required"
            }, choices=[
                ('', ''),
                ('M', 'Masculino'),
                ('F', 'Feminino'),
                ('O', 'Outro')
            ]),
        }

    def clean_password(self):
        cleaned_data = self.cleaned_data
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm:
            if password != password_confirm:
                raise forms.ValidationError("As senhas não coincidem")
        return cleaned_data
    
    def clean_email(self):
        email = self.cleaned_data.get("email")

        if Paciente.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email já está em uso.")
        
        return email    

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