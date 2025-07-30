from django import forms
from django.forms import ModelForm, DateInput
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password
from users.models import Paciente, Medico, Administrador, Usuario
from dashboard.models import CriarEvento, MembroEvento

class PacienteForm(forms.ModelForm):
    avatar = forms.ImageField(required=False)
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': "input validator", 'type': "password", 'placeholder': "Senha", 'minlength': "8", 'title': "Must be more than 8 characters, including number, lowercase letter, uppercase letter"
    }),
    validators = [validate_password],
    )
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': "input validator", 'type': "password", 'placeholder': "Confirme a Senha", 'minlength': "8", 'title': "Must be more than 8 characters, including number, lowercase letter, uppercase letter"
    }),
    validators = [validate_password],
    )

    class Meta:
        model = Paciente
        fields = ['avatar', 'email', 'username', 'data_nascimento', 'telefone', 'genero']
        widgets = {
            'username': forms.TextInput(attrs={
                'type': 'text',
                'class': "input validator",
                'name': 'username',
                'required': 'required',
                'placeholder': 'Nome',
                'minlength': '3',
                'title': 'Must be more than 3 characters, only letters and spaces'
            }),
            'email': forms.EmailInput(attrs={
                'type': 'email',
                'class': "input validator",
                'placeholder': 'exemplo@gmail.com',
                'required': 'required'
            }),
            'data_nascimento': forms.DateInput(attrs={
                'type': "date",
                'class': "input validator",
                'min': "1935-01-01",
                'max': "2025-12-31",
                'title': "Must be valid"
            },
            format='%Y-%m-%d'
            ),
            'telefone': forms.TextInput(attrs={
                'type': "tel",
                "id": "telefone",
                'placeholder': "Telefone",
                'class': "input validator tabular-nums",
                'required': "required"
            }),
            'genero': forms.Select(attrs={
                'class': "select validator",
                'required': "required"
            }, choices=[
                ('', ''),
                ('M', 'Masculino'),
                ('F', 'Feminino'),
                ('O', 'Outro')
            ]),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['password'].required = False
            self.fields['password_confirm'].required = False    
        if self.instance and self.instance.data_nascimento:
            self.initial['data_nascimento'] = self.instance.data_nascimento.strftime('%Y-%m-%d')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password or password_confirm:
            if password != password_confirm:
                self.add_error('password_confirm', "As senhas não coincidem")
        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get("username")

        qs = Usuario.objects.filter(username=username)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Este nome já está em uso.")
        return username
    
    def clean_telefone(self):
        telefone = self.cleaned_data.get("telefone")
        if len(telefone) < 13:
            raise forms.ValidationError("O telefone deve conter 10 ou 11 dígitos.")
        return telefone    
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs = Usuario.objects.filter(email=email)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Este email já está em uso.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user

class MedicoForm(forms.ModelForm):
    avatar = forms.ImageField(required=False)
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': "input validator", 'type': "password", 'placeholder': "Senha", 'minlength': "8", 'title': "Must be more than 8 characters, including number, lowercase letter, uppercase letter"
    }),
    validators = [validate_password],
    )
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': "input validator", 'type': "password", 'placeholder': "Confirme a Senha", 'minlength': "8", 'title': "Must be more than 8 characters, including number, lowercase letter, uppercase letter"
    }),
    validators = [validate_password],
    )

    class Meta:
        model = Medico
        fields = ['avatar', 'email', 'username', 'especialidade', 'data_nascimento', 'telefone', 'genero']
        widgets = {
            'username': forms.TextInput(attrs={
                'type': 'text',
                'class': "input validator",
                'name': 'username',
                'required': 'required',
                'placeholder': 'Nome',
                'minlength': '3',
                'title': 'Must be more than 3 characters, only letters and spaces'
            }),
            'email': forms.EmailInput(attrs={
                'type': 'email',
                'class': "input validator",
                'placeholder': 'exemplo@gmail.com',
                'required': 'required'
            }),
             'especialidade': forms.Select(attrs={
                'class': "select validator",
                'required': "required"
            }, choices=[
                ('Selecione', ''),
                ('Anestesiologia', 'Anestesiologia'),
                ('Angiologia', 'Angiologia'),
                ('Cardiologia', 'Cardiologia'),
                ('Coloproctologia', 'Coloproctologia'),
                ('Dermatologia', 'Dermatologia')
            ]),
            'data_nascimento': forms.DateInput(attrs={
                'type': "date",
                'class': "input validator",
                'min': "1935-01-01",
                'max': "2025-12-31",
                'title': "Must be valid"
            }),
            'telefone': forms.TextInput(attrs={
                'type': "tel",
                "id": "telefone",
                'placeholder': "Telefone",
                'class': "input validator tabular-nums",
                'required': "required"
            }),
            'genero': forms.Select(attrs={
                'class': "select validator",
                'required': "required"
            }, choices=[
                ('', ''),
                ('M', 'Masculino'),
                ('F', 'Feminino'),
                ('O', 'Outro')
            ]),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['password'].required = False
            self.fields['password_confirm'].required = False   
        if self.instance and self.instance.data_nascimento:
            self.initial['data_nascimento'] = self.instance.data_nascimento.strftime('%Y-%m-%d')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password or password_confirm:
            if password != password_confirm:
                self.add_error('password_confirm', "As senhas não coincidem")
        return cleaned_data
    
    def clean_username(self):
        username = self.cleaned_data.get("username")

        qs = Usuario.objects.filter(username=username)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Este nome já está em uso.")
        return username

    def clean_telefone(self):
        telefone = self.cleaned_data.get("telefone")
        if len(telefone) < 13:
            raise forms.ValidationError("O telefone deve conter 10 ou 11 dígitos.")
        return telefone    
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs = Usuario.objects.filter(email=email)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Este email já está em uso.")
        return email
    
    def __str__(self):
        return f"Dr(a). {self.username}"

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user

class AdministradorForm(forms.ModelForm):
    avatar = forms.ImageField(required=False)
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': "input validator", 'type': "password", 'placeholder': "Senha", 'minlength': "8", 'title': "Must be more than 8 characters, including number, lowercase letter, uppercase letter"
    }),
    validators = [validate_password],
    )
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': "input validator", 'type': "password", 'placeholder': "Confirme a Senha", 'minlength': "8", 'title': "Must be more than 8 characters, including number, lowercase letter, uppercase letter"
    }),
    validators = [validate_password],
    )

    class Meta:
        model = Administrador
        fields = ['avatar', 'email', 'username']
        widgets = {
            'username': forms.TextInput(attrs={
                'type': 'text',
                'class': "input validator",
                'name': 'username',
                'required': 'required',
                'placeholder': 'Nome',
                'minlength': '3',
                'title': 'Must be more than 3 characters, only letters and spaces'
            }),
            'email': forms.EmailInput(attrs={
                'type': 'email',
                'class': "input validator",
                'placeholder': 'exemplo@gmail.com',
                'required': 'required'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['password'].required = False
            self.fields['password_confirm'].required = False    

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password or password_confirm:
            if password != password_confirm:
                self.add_error('password_confirm', "As senhas não coincidem")
        return cleaned_data
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs = Usuario.objects.filter(email=email)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Este email já está em uso.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")
        if password:
            user.set_password(password)
        if commit:
            user.is_staff = True
            user.is_superuser = True
            user.save()
        return user

class AgendamentoForm(ModelForm):
    class Meta:
        model = CriarEvento
        fields = ["paciente", "procedimentos", "convenio", "observacoes", "data_inicio", "data_fim"]
        widgets = {
            "paciente": forms.Select(attrs={"class": "select validator", "required": "required"}),
            "procedimentos": forms.Select(attrs={"class": "select validator", "required": "required", "placeholder": "Procedimentos"}, choices=[
                ('', 'Selecione um Procedimento'),
                ('Consulta', 'Consulta'),
                ('Exame', 'Exame'),
                ('Retorno', 'Retorno'),
                ('Outro', 'Outro')
            ]),
            "convenio": forms.Select(attrs={"class": "select validator", "required": "required"}, choices=[
                ('', 'Selecione um Convênio'),
                ('Publico', 'Público'),
                ('Particular', 'Particular')
            ]),
            "observacoes": forms.Textarea(attrs={"class": "textarea", "placeholder": "Observações"}),
            "data_inicio": DateInput(attrs={"type": "datetime-local", "class": "input validator"}, format="%Y-%m-%dT%H:%M"),
            "data_fim": DateInput(attrs={"type": "datetime-local", "class": "input validator"}, format="%Y-%m-%dT%H:%M"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["data_inicio"].input_formats = ("%Y-%m-%dT%H:%M",)
        self.fields["data_fim"].input_formats = ("%Y-%m-%dT%H:%M",)

class MembroForm(forms.ModelForm):
    class Meta:
        model = MembroEvento
        fields = ["paciente"]