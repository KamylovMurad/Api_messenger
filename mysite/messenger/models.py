import uuid
from django.db import models
from django.contrib.auth.models import User


class UserToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    chat_id = models.IntegerField(unique=True, null=True)
    token = models.UUIDField(default=uuid.uuid4, unique=True)

    def __str__(self):
        return f'Token {self.user}'


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message {self.user}'

