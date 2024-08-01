from django.db import models
from django_project.common.models import BaseModel

from django.contrib.auth.models import AbstractBaseUser, Group
from django.contrib.auth.models import BaseUserManager as BUM
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator, MinLengthValidator
from django.contrib.auth.validators import UnicodeUsernameValidator


phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
            message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")


class BaseUserManager(BUM):
    def create_user(self, username, email=None, phone=None, is_active=True, is_admin=False, password=None):
        if not username:
            raise ValueError("Users must have an username")

        if email:
            user = self.model(username=username, email=email, is_active=is_active, is_admin=is_admin)
        elif phone:
            user = self.model(username=username, phone=phone, is_active=is_active, is_admin=is_admin)
        else:
            user = self.model(username=username, is_active=is_active, is_admin=is_admin)

        if password is not None:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self._db)

        return user

    def create_superuser(self, username, password=None):
        user = self.create_user(
            username=username,
            is_active=True,
            is_admin=True,
            password=password,
        )

        user.is_superuser = True
        user.save(using=self._db)

        return user


class BaseUser(BaseModel, AbstractBaseUser, PermissionsMixin):
    class StatusDefaultTwoFactor(models.TextChoices):
        GOOGLE = 'G', 'Google authenticator'
        EMAIL = 'E', 'Email'
        PHONE = 'P', 'Phone'


    class LevelUser(models.TextChoices):
        BASE = 'B', 'Base user'
        PREMIUM = 'P', 'premium'

    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )

    email = models.EmailField(verbose_name = "email address", unique=True, null=True, blank=True)
    phone = models.CharField(max_length=15, verbose_name = "phone number",
                             validators=[phone_regex],
                             unique=True, null=True, blank=True)
    google_secret = models.CharField(max_length=20, verbose_name = "phone number",
                                     unique=True, null=True, blank=True)

    level_user = models.CharField(max_length=1,
                                  choices=LevelUser.choices,
                                  default='B')

    failed_attempts_number_for_login = models.PositiveSmallIntegerField(default=0)
    two_factor_on = models.BooleanField(default=False)
    default_two_factor = models.CharField(max_length=1,
                                          choices=StatusDefaultTwoFactor.choices,
                                          default='P'
    )

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )

    objects = BaseUserManager()
    USERNAME_FIELD = "username"

    def __str__(self):
        return self.username

    def is_staff(self):
        return self.is_staff


class Profile(models.Model):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE)
    bio = models.CharField(max_length=1000, null=True, blank=True)
    def __str__(self):
        return f"{self.user} >> {self.bio}"



class PermissionsName(models.Model):
    name = models.CharField(max_length=255)
    groups = models.ManyToManyField(Group, related_name='permissions_names',
                                    related_query_name='permissions_name',
                                    blank=True,
    )
    category = models.CharField(max_length=255, null=True)
    def __str__(self):
        return self.category + '>' + self.name



