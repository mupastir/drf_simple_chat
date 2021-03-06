from django.db import models

from config.django_utils.models import UUIDTimeStampModel
from users.models import User


class Thread(UUIDTimeStampModel):
    participants = models.ManyToManyField(User, related_name='participants')

    def __str__(self):
        return f'{self.id}'


class Message(UUIDTimeStampModel):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.created}|{self.sender}|{self.text[:10]}...'
