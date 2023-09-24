from django.contrib import admin
from .models import UserToken


@admin.register(UserToken)
class UserTokenAdmin(admin.ModelAdmin):
    pass

