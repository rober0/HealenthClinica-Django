from django import forms
from .models import Contato, Sugestao


class ContatoForm(forms.ModelForm):
    class Meta:
        model = Contato
        fields = ["nome", "email", "categoria"]

        widgets = {
            "nome": forms.TextInput(
                attrs={
                    "type": "text",
                    "class": "input validator",
                    "placeholder": "Digite seu nome completo",
                    "minlength": "3",
                    "required": "required",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "exemplo@email.com",
                    "class": "input validator",
                    "autocomplete": "email",
                    "required": "required",
                }
            ),
            "categoria": forms.Select(
                attrs={
                    "class": "input validator",
                    "required": "required",
                }
            ),
        }


class SugestoesForm(forms.ModelForm):
    class Meta:
        model = Sugestao
        fields = [
            "nome",
            "email",
            "sugestao",
        ]

        widgets = {
            "nome": forms.TextInput(
                attrs={
                    "type": "text",
                    "class": "input validator",
                    "placeholder": "Digite seu nome completo",
                    "minlength": "3",
                    "required": "required",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "exemplo@email.com",
                    "class": "input validator",
                    "autocomplete": "email",
                    "required": "required",
                }
            ),
            "sugestao": forms.Textarea(
                attrs={
                    "placeholder": "...",
                    "rows": 4,
                    "class": "input validator",
                    "required": "required",
                }
            ),
        }
