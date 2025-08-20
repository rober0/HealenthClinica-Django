from django import forms
from .models import Contato, Sugestao


class ContatoForm(forms.ModelForm):
    class Meta:
        model = Contato
        fields = ["solicitanteC", "nomeC", "emailC", "categoria", "comentarios"]

        widgets = {
            "solicitanteC": forms.Select(
                attrs={"class": "input validator", "required": "required",
                       }
            ),
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
                attrs={"class": "input validator", "required": "required",
                }
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
            "solicitanteC": {"required": "selecione o solicitante"},
            "nomeC": {"required": "Insira um nome válido"},
            "emailC": {
                "required": "Por favor, informe seu e-mail",
                "invalid": "Digite um e-mail válido",
            },
            "categoria": {"required": "Por favor, selecione uma categoria"},
            "comentarios": {"required": "Por favor, descreva seu assunto"},
        }


class SugestoesForm(forms.ModelForm):
    class Meta:
        model = Sugestao
        fields = ["solicitanteS", "nomeS", "emailS", "procedimentosS", "convenio", "observacoes"]

        widgets = {
            "solicitanteS": forms.Select(
                attrs={"class": "input validator", "required": "required",
                       }
            ),
            "nomeS": forms.TextInput(
                attrs={
                    "type": "text",
                    "class": "input validator",
                    "placeholder": "Digite seu nome completo",
                    "minlength": "3",
                    "required": "required",
                }
            ),
            "emailS": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "exemplo@email.com",
                    "class": "input validator",
                    "autocomplete": "email",
                    "required": "required",
                }
            ),
            "procedimentosS": forms.Select(
                attrs={"class": "input validator", "required": "required",
                }
            ),
            "convenio": forms.Select(
                attrs={"class": "input validator", "required": "required",
                }
            ),
            "observacoes": forms.Textarea(
                attrs={
                    "placeholder": "...",
                    "rows": 4,
                    "class": "input validator",
                    "required": "required",
                }
            ),
        }

        error_messages = {
            "solicitanteS": {"required": "selecione o solicitante"},
            "nomeS": {"required": "Insira um nome válido"},
            "emailS": {
                "required": "Por favor, informe seu e-mail",
                "invalid": "Digite um e-mail válido",
            },
            "procedimentosS": {"required": "Por favor, selecione um procedimento válido"},
            "convenio": {"required": "Por favor, selecione uma convênio válido"},
            "observacoes": {"required": "Por favor, descreva seu assunto"},
        }
