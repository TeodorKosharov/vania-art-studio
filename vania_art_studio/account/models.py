from django.db import models
from vania_art_studio.account.managers import AppUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from vania_art_studio.account.validators import username_validator, first_name_validator, last_name_validator, \
    city_validator
from cloudinary.models import CloudinaryField


class AppUser(AbstractBaseUser, PermissionsMixin):
    USERNAME_MAX_LENGTH = 20

    username = models.CharField(max_length=USERNAME_MAX_LENGTH, unique=True, null=False, blank=False, validators=(
        username_validator,
    ))
    email = models.EmailField(null=False, blank=False)
    is_staff = models.BooleanField(default=False)

    objects = AppUserManager()

    USERNAME_FIELD = 'username'


class Profile(models.Model):
    FIRST_NAME_MAX_LENGTH = 20
    LAST_NAME_MAX_LENGTH = 20
    CITY_MAX_LENGTH = 30

    first_name = models.CharField(max_length=FIRST_NAME_MAX_LENGTH, null=True, blank=True,
                                  validators=(first_name_validator,))
    last_name = models.CharField(max_length=LAST_NAME_MAX_LENGTH, null=True, blank=True,
                                 validators=(last_name_validator,))
    age = models.PositiveIntegerField(null=True, blank=True)
    city = models.CharField(max_length=CITY_MAX_LENGTH, null=True, blank=True, validators=(
        city_validator,
    ))
    profile_picture = CloudinaryField('image')
    user = models.OneToOneField(AppUser, primary_key=True, on_delete=models.CASCADE, related_name='profile')
