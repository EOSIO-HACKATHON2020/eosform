import logging
from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TimeStampedModel


logger = logging.getLogger(__name__)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not email:
            raise ValueError('email must be set')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(PermissionsMixin, TimeStampedModel, AbstractBaseUser):
    email = models.EmailField(
        _('Email'),
        max_length=254,
        unique=True,
        db_index=True,
        null=True,
        blank=True,
        help_text=_('Required. 254 characters or fewer. '
                    'Letters, digits and @/./+/-/_ only.'),
        validators=[
            validators.RegexValidator(
                r'^[\w.@+-]+$',
                _('Enter a valid username. This value may contain only '
                  'letters, numbers ' 'and @/./+/-/_ characters.')
            ),
        ],
    )
    first_name = models.CharField(_('First name'), max_length=50, null=True,
                                  blank=True)
    last_name = models.CharField(_('Last name'), max_length=50, null=True,
                                 blank=True)

    is_staff = models.BooleanField(
        _('Staff status'),
        default=False,
        help_text=_('Designates whether the user '
                    'can log into this admin site.'),
    )

    is_active = models.BooleanField(
        _('Active'),
        default=True,
    )

    def get_full_name(self):
        """
        Returns the first_name, the middle_name
        and the last_name, with a space in between.
        """
        full_name = f'{self.first_name} {self.last_name}'
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    def email_user(self, subject, message, html_message=None,
                   from_email=settings.DEFAULT_FROM_EMAIL):
        """
        Sends an email to this user.
        """
        mail_kwargs = {
            'subject': subject,
            'message': message,
            'html_message': html_message,
            'from_email': from_email,
            'to': [self.email]
        }
        # logger.info(mail_kwargs)
        print(mail_kwargs)
        from .tasks import send_email
        send_email.apply_async(kwargs=mail_kwargs)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def full_clean(self, *args, **kwargs):
        if not self.email:
            raise ValidationError(_('Email cannot be blank.'))
        if self.email == '':
            raise ValidationError(_('Email can not be empty.'))
        super().full_clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.email)

    class Meta:
        db_table = 'users'
