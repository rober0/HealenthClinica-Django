from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):

    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email é obrigatório')
        
        email = self.normalize_email(email)
        user = self.model(
            username=username, 
            email=email, 
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username=username, email=email, password=password, **extra_fields)

class AbstractUsuario(AbstractUser):
    email = models.EmailField(_('Email'), unique=True)
    username = models.CharField(_('username'), max_length=255, unique=True,)
    
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=_('groups'),
        blank=True,
        help_text=_('The groups this user belongs to.'),
        related_name="%(app_label)s_%(class)s_groups",
        related_query_name="%(app_label)s_%(class)s",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="%(app_label)s_%(class)s_permissions",
        related_query_name="%(app_label)s_%(class)s",
    )

    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        abstract = True

class Administrador(AbstractUsuario):
    class Meta:
        verbose_name = 'Administrador'
        verbose_name_plural = 'Administradores'

    def __str__(self):
        return self.username

class Paciente(AbstractUsuario):
    cpf = models.CharField(max_length=11, unique=True)
    data_nascimento = models.DateField(null=True, blank=True)
    numero = models.CharField(max_length=15)
    genero = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'

    def __str__(self):
        return self.username

class Medico(AbstractUsuario):
    especialidade = models.CharField(max_length=100)
    data_nascimento = models.DateField(null=True, blank=True)
    numero = models.CharField(max_length=15)
    genero = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'Médico'
        verbose_name_plural = 'Médicos'

    def __str__(self):
        return f"Dr(a). {self.username}"