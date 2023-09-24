import asgiref
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


from .models import UserToken
from .serializers import RegisterSerializer, TokenSerializers, ChatSerializers, MessageSerializer
from bot import bot


class RegisterView(CreateAPIView):
    """
    Создание нового пользователя.
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (~IsAuthenticated,)

    def perform_create(self, serializer) -> None:
        user = serializer.save()
        login(self.request, user)
        UserToken.objects.create(user=user)


class UserTokenCreateView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TokenSerializers

    def get_queryset(self):
        user = self.request.user
        token = UserToken.objects.filter(user=user)
        return token


class UserChat_idView(CreateAPIView):
    serializer_class = ChatSerializers

    def post(self, request, *args, **kwargs):
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
    serializer_class = MessageSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user
        text = request.data['message']
        text = f'{user}, я получил от тебя сообщение:\n{text}'
        try:
            user = UserToken.objects.get(user=user)

            asgiref.sync.async_to_sync(bot.send_message)(user.chat_id, text)

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