from email.headerregistry import Group
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin, Group
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        
        email = self.normalize_email(email)   
        grupo = extra_fields.pop("grupo", None)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        
        user = self.model(
            email=email,
            username=username,
            grupo=grupo,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_medico(self, email, username, password=None, **extra_fields):
        user = self.create_user(email, username, **extra_fields)
        try:
            medico_group = Group.objects.get(Name='Medico')
            user.groups.add(medico_group)
        except Group.DoesNotExist:
            print("O grupo 'Medico' não existe.")
        return user

    def create_paciente(self, email, username, password=None, **extra_fields):
        user = self.create_user(email, username, **extra_fields)
        try:
            paciente_group = Group.objects.get(Name='Paciente')
            user.groups.add(paciente_group)
        except Group.DoesNotExist:
            print("O grupo 'Paciente' não existe.")
        return user

    def create_staffuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", False)
        return self.create_user(email, username, password, **extra_fields)

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, username, password, **extra_fields)

class Usuario(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name= _("Email"),
        max_length=255,
        unique=True,
    )
    username = models.CharField(
        verbose_name=_("Username"),
        max_length=150,
        unique=True,
    )
    grupo = models.ForeignKey(
        Group,
        verbose_name=_("Grupo"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(_("Active"),default=True)
    is_staff = models.BooleanField(_("Staff Status"),default=False)
    is_superuser = models.BooleanField(_("Super User Status"), default=False)
    date_joined = models.DateTimeField(_("Date Joined"), auto_now_add=True)
    last_updated = models.DateTimeField(_("Last Updated"), auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = _('usuário')
        verbose_name_plural = _('usuários')

    def __str__(self):
        return self.email

    def get_group_name(self):
        group = self.groups.first()
        return group.name if group else "Sem grupo"    
    
    def save(self, *args, **kwargs):
        if not self.grupo and self.groups.exists():
            self.grupo = self.groups.first()
        super().save(*args, **kwargs)