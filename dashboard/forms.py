from django import forms
from django.forms import ModelForm, DateInput
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from users.models import Paciente, Medico, Administrador, Usuario
from dashboard.models import CriarEvento, BloquearDia


class PacienteForm(forms.ModelForm):
    avatar = forms.ImageField(required=False)
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "input validator",
                "type": "password",
                "placeholder": "Senha",
                "minlength": "8",
                "title": "Must be more than 8 characters, including number, lowercase letter, uppercase letter",
            }
        ),
        validators=[validate_password],
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "input validator",
                "type": "password",
                "placeholder": "Confirme a Senha",
                "minlength": "8",
                "title": "Must be more than 8 characters, including number, lowercase letter, uppercase letter",
            }
        ),
        validators=[validate_password],
    )

    class Meta:
        model = Paciente
        fields = [
            "avatar",
            "email",
            "username",
            "data_nascimento",
            "telefone",
            "genero",
        ]
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "type": "text",
                    "class": "input validator",
                    "name": "username",
                    "required": "required",
                    "placeholder": "Nome",
                    "minlength": "3",
                    "title": "Must be more than 3 characters, only letters and spaces",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "type": "email",
                    "class": "input validator",
                    "placeholder": "exemplo@gmail.com",
                    "required": "required",
                }
            ),
            "data_nascimento": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "input validator",
                    "min": "1935-01-01",
                    "max": "2025-12-31",
                    "title": "Must be valid",
                },
                format="%Y-%m-%d",
            ),
            "telefone": forms.TextInput(
                attrs={
                    "type": "tel",
                    "id": "telefone",
                    "placeholder": "Telefone",
                    "class": "input validator tabular-nums",
                    "required": "required",
                }
            ),
            "genero": forms.Select(
                attrs={"class": "select validator", "required": "required"},
                choices=[
                    ("", "Selecione"),
                    ("Masculino", "Masculino"),
                    ("Feminino", "Feminino"),
                    ("Outro", "Outro"),
                ],
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["password"].required = False
            self.fields["password_confirm"].required = False
        if self.instance and self.instance.data_nascimento:
            self.initial["data_nascimento"] = self.instance.data_nascimento.strftime(
                "%Y-%m-%d"
            )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password or password_confirm:
            if password != password_confirm:
                self.add_error("password_confirm", "As senhas não coincidem")
        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if not username:
            raise forms.ValidationError("Nome de usuário é obrigatório.")

        upper_username = username.upper()

        if (
            Usuario.objects.filter(username=upper_username)
            .exclude(pk=self.instance.pk)
            .exists()
        ):
            raise forms.ValidationError("Este nome de usuário já está em uso.")

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
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "input validator",
                "type": "password",
                "placeholder": "Senha",
                "minlength": "8",
                "title": "Must be more than 8 characters, including number, lowercase letter, uppercase letter",
            }
        ),
        validators=[validate_password],
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "input validator",
                "type": "password",
                "placeholder": "Confirme a Senha",
                "minlength": "8",
                "title": "Must be more than 8 characters, including number, lowercase letter, uppercase letter",
            }
        ),
        validators=[validate_password],
    )

    class Meta:
        model = Medico
        fields = [
            "avatar",
            "email",
            "username",
            "especialidade",
            "crm_estado",
            "crm_numero",
            "data_nascimento",
            "telefone",
            "genero",
        ]
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "type": "text",
                    "class": "input validator",
                    "name": "username",
                    "required": "required",
                    "placeholder": "Nome",
                    "minlength": "3",
                    "title": "Must be more than 3 characters, only letters and spaces",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "type": "email",
                    "class": "input validator",
                    "placeholder": "exemplo@gmail.com",
                    "required": "required",
                }
            ),
            "especialidade": forms.Select(
                attrs={"class": "select validator", "required": "required"},
                choices=[
                    ("", "Selecione"),
                    ("Anestesiologia", "Anestesiologia"),
                    ("Angiologia", "Angiologia"),
                    ("Cardiologia", "Cardiologia"),
                    ("Coloproctologia", "Coloproctologia"),
                    ("Dermatologia", "Dermatologia"),
                ],
            ),
            "crm_estado": forms.Select(
                attrs={"class": "select validator", "required": "required"},
                choices=[
                    ("", "Selecione"),
                    ("CRM/AC", "CRM/AC"),
                    ("CRM/AL", "CRM/AL"),
                    ("CRM/AM", "CRM/AM"),
                    ("CRM/AP", "CRM/AP"),
                    ("CRM/BA", "CRM/BA"),
                    ("CRM/CE", "CRM/CE"),
                    ("CRM/DF", "CRM/DF"),
                    ("CRM/ES", "CRM/ES"),
                    ("CRM/GO", "CRM/GO"),
                    ("CRM/MA", "CRM/MA"),
                    ("CRM/MG", "CRM/MG"),
                    ("CRM/MS", "CRM/MS"),
                    ("CRM/MT", "CRM/MT"),
                    ("CRM/PA", "CRM/PA"),
                    ("CRM/PB", "CRM/PB"),
                    ("CRM/PE", "CRM/PE"),
                    ("CRM/PI", "CRM/PI"),
                    ("CRM/RJ", "CRM/RJ"),
                    ("CRM/RN", "CRM/RN"),
                    ("CRM/RO", "CRM/RO"),
                    ("CRM/RR", "CRM/RR"),
                    ("CRM/RS", "CRM/RS"),
                    ("CRM/SC", "CRM/SC"),
                    ("CRM/SP", "CRM/SP"),
                    ("CRM/SE", "CRM/SE"),
                    ("CRM/TO", "CRM/TO"),
                ],
            ),
            "crm_numero": forms.TextInput(
                attrs={
                    "type": "text",
                    "inputmode": "numeric",
                    "class": "input validator",
                    "pattern": "[0-9]{6}",
                    "placeholder": "Número",
                    "required": "required",
                    "maxlength": "6",
                    "title": "Digite o número do CRM",
                }
            ),
            "data_nascimento": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "input validator",
                    "min": "1935-01-01",
                    "max": "2025-12-31",
                    "title": "Must be valid",
                }
            ),
            "telefone": forms.TextInput(
                attrs={
                    "type": "tel",
                    "id": "telefone",
                    "placeholder": "Telefone",
                    "class": "input validator tabular-nums",
                    "required": "required",
                }
            ),
            "genero": forms.Select(
                attrs={"class": "select validator", "required": "required"},
                choices=[
                    ("", "Selecione"),
                    ("Masculino", "Masculino"),
                    ("Feminino", "Feminino"),
                    ("Outro", "Outro"),
                ],
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["password"].required = False
            self.fields["password_confirm"].required = False
        if self.instance and self.instance.data_nascimento:
            self.initial["data_nascimento"] = self.instance.data_nascimento.strftime(
                "%Y-%m-%d"
            )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password or password_confirm:
            if password != password_confirm:
                self.add_error("password_confirm", "As senhas não coincidem")
        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if not username:
            raise forms.ValidationError("Nome de usuário é obrigatório.")

        upper_username = username.upper()

        if (
            Usuario.objects.filter(username=upper_username)
            .exclude(pk=self.instance.pk)
            .exists()
        ):
            raise forms.ValidationError("Este nome de usuário já está em uso.")

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

    def clean_crm(self):
        crm_numero = self.cleaned_data.get("crm_numero")
        crm_estado = self.cleaned_data.get("crm_estado")
        if not crm_numero or not crm_estado:
            raise forms.ValidationError("CRM Número e Estado são obrigatórios.")

        qs = Medico.objects.filter(crm_numero=crm_numero, crm_estado=crm_estado)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Este CRM já está em uso.")
        return crm_numero

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
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "input validator",
                "type": "password",
                "placeholder": "Senha",
                "minlength": "8",
                "title": "Must be more than 8 characters, including number, lowercase letter, uppercase letter",
            }
        ),
        validators=[validate_password],
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "input validator",
                "type": "password",
                "placeholder": "Confirme a Senha",
                "minlength": "8",
                "title": "Must be more than 8 characters, including number, lowercase letter, uppercase letter",
            }
        ),
        validators=[validate_password],
    )

    class Meta:
        model = Administrador
        fields = ["avatar", "email", "username"]
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "type": "text",
                    "class": "input validator",
                    "name": "username",
                    "required": "required",
                    "placeholder": "Nome",
                    "minlength": "3",
                    "title": "Must be more than 3 characters, only letters and spaces",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "type": "email",
                    "class": "input validator",
                    "placeholder": "exemplo@gmail.com",
                    "required": "required",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["password"].required = False
            self.fields["password_confirm"].required = False

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password or password_confirm:
            if password != password_confirm:
                self.add_error("password_confirm", "As senhas não coincidem")
        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if not username:
            raise forms.ValidationError("Nome de usuário é obrigatório.")

        upper_username = username.upper()

        if (
            Usuario.objects.filter(username=upper_username)
            .exclude(pk=self.instance.pk)
            .exists()
        ):
            raise forms.ValidationError("Este nome de usuário já está em uso.")

        return username

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
        fields = [
            "paciente",
            "medico",
            "procedimentos",
            "convenio",
            "observacoes",
            "status",
            "data_inicio",
            "data_fim",
        ]
        widgets = {
            "paciente": forms.Select(attrs={"class": "select validator", "required": "required"}),
            "medico": forms.Select(attrs={"class": "select validator"}),
            "procedimentos": forms.Select(attrs={"class": "select validator", "required": "required"}),
            "convenio": forms.Select(attrs={"class": "select validator", "required": "required"}),
            "observacoes": forms.Textarea(attrs={"class": "textarea", "placeholder": "Observações", "style": "height: 15px;"}),
            "status": forms.Select(attrs={"class": "select validator", "required": "required"}),
            "data_inicio": DateInput(attrs={"type": "datetime-local", "class": "input validator"}, format="%Y-%m-%dT%H:%M"),
            "data_fim": DateInput(attrs={"type": "datetime-local", "class": "input validator"}, format="%Y-%m-%dT%H:%M"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['medico'].required = False
        self.fields['status'].required = False
        self.fields["data_inicio"].input_formats = ("%Y-%m-%dT%H:%M",)
        self.fields["data_fim"].input_formats = ("%Y-%m-%dT%H:%M",)

    def clean(self):
        cleaned_data = super().clean()
        data_inicio = cleaned_data.get("data_inicio")
        data_fim = cleaned_data.get("data_fim")
        medico = cleaned_data.get("medico")

        if not medico:
            raise ValidationError("O médico responsável precisa ser especificado.")

        if data_inicio and data_fim:
            if data_fim <= data_inicio:
                raise ValidationError("A data final deve ser posterior à data inicial.")

            conflitos = CriarEvento.objects.filter(
                medico=medico,
                data_inicio__lt=data_fim,
                data_fim__gt=data_inicio,
                is_deleted=False
            )
            if self.instance and self.instance.pk:
                conflitos = conflitos.exclude(pk=self.instance.pk)

            if conflitos.exists():
                self._is_conflict = True
                raise ValidationError("Conflito de horário! Este período já está agendado.")
        
        return cleaned_data

class MarcarAgendamentoForm(ModelForm):
    class Meta:
        model = CriarEvento
        fields = [
            "medico",
            "convenio",
            "queixa",
            "data_inicio",
            "data_fim",
        ]
        widgets = {
            "medico": forms.Select(
                attrs={"class": "select validator", "required": "required"}
            ),
            "convenio": forms.Select(
                attrs={"class": "select validator", "required": "required"}
            ),
            "queixa": forms.Textarea(
                attrs={
                    "class": "textarea",
                    "placeholder": "Observações",
                    "style": "height: 15px;",
                }
            ),
            "data_inicio": DateInput(
                attrs={"type": "datetime-local", "class": "input validator"},
                format="%Y-%m-%dT%H:%M",
            ),
            "data_fim": DateInput(
                attrs={"type": "datetime-local", "class": "input validator"},
                format="%Y-%m-%dT%H:%M",
            ),
        }


class BloquearDiaForm(ModelForm):
    class Meta:
        model = BloquearDia
        fields = ["dia_escolhido", "horario_inicio", "horario_fim"]
        widgets = {
            "dia_escolhido": forms.Select(
                attrs={"class": "select validator", "required": "required"},
            ),
            "horario_inicio": forms.TimeInput(
                attrs={
                    "type": "time",
                    "class": "input validator",
                    "required": "required",
                },
            ),
            "horario_fim": forms.TimeInput(
                attrs={
                    "type": "time",
                    "class": "input validator",
                    "required": "required",
                },
            ),
        }
