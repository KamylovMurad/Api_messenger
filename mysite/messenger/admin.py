from django.contrib import admin
from .models import UserToken, Message


@admin.register(UserToken)
class UserTokenAdmin(admin.ModelAdmin):
    pass


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    pass
