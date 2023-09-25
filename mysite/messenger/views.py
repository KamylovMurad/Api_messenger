from typing import List
import asgiref
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.http import HttpResponse
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


from .models import UserToken, Message
from .serializers import (
    RegisterSerializer,
    TokenSerializers,
    ChatSerializers,
    MessageSerializer,
    AllMessagesSerializer
)
from bot import bot


class RegisterView(CreateAPIView):
    """
    View for creating a new user.

    Attributes:
        queryset (QuerySet): The queryset for user objects.
        serializer_class (RegisterSerializer): The serializer class for user registration.
        permission_classes (tuple): Tuple of permission classes for the view (~IsAuthenticated).

    Methods:
        perform_create(self, serializer) -> None: Create a new user and associated UserToken.
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (~IsAuthenticated,)

    def perform_create(self, serializer) -> None:
        """
        Create a new user and associated UserToken.

        Args:
            serializer (RegisterSerializer): The serializer instance with user data.

        Returns:
            None
        """
        user = serializer.save()
        login(self.request, user)
        UserToken.objects.create(user=user)


class UserTokenCreateView(ListAPIView):
    """
    View for listing user tokens.

    Attributes:
        permission_classes (tuple): Tuple of permission classes for the view.
        serializer_class (TokenSerializers): The serializer class for token objects.

    Methods:
        get_queryset(self): Get the queryset of user tokens for the current user.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = TokenSerializers

    def get_queryset(self) -> List[UserToken]:
        """
        Get the queryset of user tokens for the current user.

        Returns:
            List[UserToken]: List of user tokens.
        """
        user = self.request.user
        token = UserToken.objects.filter(user=user)
        return token


class UserChat_idView(CreateAPIView):
    """
    View for creating and updating user chat IDs.

    Attributes:
        serializer_class (ChatSerializers): The serializer class for chat ID objects.

    Methods:
        post(self, request, *args, **kwargs): Create or update a user's chat ID.
    """
    serializer_class = ChatSerializers

    def post(self, request, *args, **kwargs) -> HttpResponse:
        """
        Create or update a user's chat ID.

        Args:
            request (Request): The HTTP request object.
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: HTTP response with a status and message.
        """
        token = request.data['token']
        try:
            user = UserToken.objects.get(token=token)
            user.chat_id = request.data['chat_id']
            user.save()
            return Response(
                {
                    'status': 'success',
                    'data': "Токен сохранен и привязан к вашему чату.",
                }
            )
        except ObjectDoesNotExist:
            return Response(
                {
                    'status': 'error',
                    'data': "Извините, но такой токен не найден.",
                }
            )
        except ValidationError:
            return Response(
                {
                    'status': 'error',
                    'data': "Неверный формат токена.",
                }
            )


class MessageView(APIView):
    """
    View for sending messages and saving them.

    Attributes:
        serializer_class (MessageSerializer): The serializer class for message objects.
        permission_classes (tuple): Tuple of permission classes for the view.

    Methods:
        post(self, request): Send a message, save it, and send it to the user's chat.
    """
    serializer_class = MessageSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request) -> HttpResponse:
        """
        Send a message, save it, and send it to the user's chat.

        Args:
            request (Request): The HTTP request object.

        Returns:
            Response: HTTP response with a status and message.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = request.user
            text = request.data['text']
            text = f'{user}, я получил от тебя сообщение:\n{text}'
            try:
                user = UserToken.objects.get(user=user)

                asgiref.sync.async_to_sync(bot.send_message)(user.chat_id, text)
                serializer.save(user=user.user)
                return Response(
                    {
                        'status': 'success',
                        'data': 'Сообщение отправлено.',
                    }
                )
            except ObjectDoesNotExist:
                return Response(
                    {
                        'status': 'error',
                        'data': "Сообщение не отправлено",
                    }
                )
            except Exception:
                return Response(
                    {
                        'status': 'error',
                        'data': "Chat id не найден.",
                    }
                )


class AllMessageView(ListAPIView):
    """
    View for listing all messages for the current user.

    Attributes:
        serializer_class (AllMessagesSerializer): The serializer class for all message objects.
        permission_classes (tuple): Tuple of permission classes for the view.

    Methods:
        get_queryset(self): Get the queryset of all messages for the current user.
    """
    serializer_class = AllMessagesSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self) -> List[Message]:
        """
        Get the queryset of all messages for the current user.

        Returns:
            List[Message]: List of message objects.
        """
        user = self.request.user
        return Message.objects.filter(user=user)
