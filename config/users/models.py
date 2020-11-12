from django.contrib.auth.models import AbstractUser

from django_utils.models import UUIDTimeStampModel


class User(UUIDTimeStampModel, AbstractUser):

    def __str__(self):
        return f'{self.first_name} {self.last_name} *{self.username}*'
