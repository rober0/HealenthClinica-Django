from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import Paciente, Medico, Administrador

class CustomUserAdmin(UserAdmin):
    ordering = ('email',)
    list_display = ('email', 'username', 'is_staff', 'is_active')
    search_fields = ('email', 'username')
    
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )

class PacienteAdmin(CustomUserAdmin):
    list_display = ('username', 'email', 'cpf', 'data_nascimento', 'numero', 'genero')
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informações Pessoais', {'fields': ('username', 'cpf', 'data_nascimento', 'numero', 'genero')}),
        ('Permissões', {'fields': ('is_active', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'cpf', 'data_nascimento', 'numero', 'genero', 'password1', 'password2'),
        }),
    )

class MedicoAdmin(CustomUserAdmin):
    list_display = ('username', 'email', 'especialidade', 'data_nascimento', 'numero', 'genero')
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informações Pessoais', {'fields': ('username', 'especialidade', 'data_nascimento', 'numero', 'genero')}),
        ('Permissões', {'fields': ('is_active', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'especialidade', 'data_nascimento', 'numero', 'genero', 'password1', 'password2'),
        }),
    )

class AdministradorAdmin(CustomUserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_superuser')
    
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_staff', 'is_superuser'),
        }),
    )

admin.site.register(Paciente, PacienteAdmin)
admin.site.register(Medico, MedicoAdmin)
admin.site.register(Administrador, AdministradorAdmin)