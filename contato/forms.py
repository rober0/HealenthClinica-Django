from django import forms
from .models import Contato


class ContatoForm(forms.ModelForm):
    class Meta:
        model = Contato
        fields = ["nomeC", "emailC", "categoria", "comentarios"]

        widgets = {
            "nomeC": forms.TextInput(
                attrs={
                    "type": "text",
                    "class": "input validator",
                    "placeholder": "Digite seu nome completo",
                    "minlength": "3",
                    "required": "required",
                }
            ),
            "emailC": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "exemplo@email.com",
                    "autocomplete": "email",
                    "required": "required",
                }
            ),
            "categoria": forms.Select(
                attrs={"class": "input validator", "required": "required"}
            ),
            "comentarios": forms.Textarea(
                attrs={
                    "placeholder": "Descreva o assunto ...",
                    "rows": 4,
                    "class": "input validator",
                    "required": "required",
                }
            ),
        }

        error_messages = {
            "nomeC": {"required": "Insira um nome válido"},
            "emailC": {
                "required": "Por favor, informe seu e-mail",
                "invalid": "Digite um e-mail válido",
            },
            "categoria": {"required": "Por favor, selecione uma categoria"},
            "comentarios": {"required": "Por favor, descreva seu assunto"},
        }
