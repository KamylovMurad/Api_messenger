from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserToken, Message


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.password = make_password(password)
        user.save()
        return user

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name']


class TokenSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserToken
        fields = ['token', ]


class ChatSerializers(serializers.ModelSerializer):
    token = serializers.CharField(write_only=True)

    class Meta:
        model = UserToken

        fields = ['token', 'chat_id', ]


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ['text', ]


class AllMessagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ['text', 'date']