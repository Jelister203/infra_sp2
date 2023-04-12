from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, **extra_fields):
        """
        Create and save a user with the given username, email.
        """
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.save()
        return user

    def create_user(self, username, email, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, **extra_fields)

    def create_superuser(self, username, email, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    User model for api_yamdb.
    Username and email are required. Other fields are optional.
    """

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_(
            '''
            Required. 150 characters or fewer.
            Letters, digits and @/./+/-/_ only.
            ''',
        ),
        validators=[username_validator],
        error_messages={
            'unique': _("User with that username already exists."),
        },
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
    )
    confirmation_code = models.CharField(max_length=10, blank=True)
    ROLE_CHOICES = [
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin'),
    ]
    role = models.CharField(max_length=9, choices=ROLE_CHOICES, default='user')
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(
        _('email address'),
        max_length=254,
        unique=True,
        blank=False,
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.',
        ),
    )

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ('username',)

    @property
    def is_admin(self):
        """Проверка на наличие прав администратора."""
        return self.role == self.admin or self.is_superuser

    @property
    def is_moderator(self):
        """Проверка на наличие прав модератора."""
        return self.role == self.moderator

    @property
    def is_user(self):
        """Проверка на наличие стандартных прав."""
        return self.role == self.user

    def __str__(self):
        return self.username
