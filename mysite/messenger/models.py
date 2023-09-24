import uuid
from django.db import models
from django.contrib.auth.models import User


class UserToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    chat_id = models.IntegerField(unique=True,  null=True)
    token = models.UUIDField(default=uuid.uuid4, unique=True)
