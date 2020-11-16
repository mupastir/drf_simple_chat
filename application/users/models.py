from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _
from django.db import models

from config.django_utils.models import UUIDTimeStampModel


class User(UUIDTimeStampModel, AbstractUser):

    def __str__(self):
        return f'{self.first_name} {self.last_name} *{self.username}*'
