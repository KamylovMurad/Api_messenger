from django.urls import path

from .views import RegisterView, UserChat_idView, UserTokenCreateView, MessageView

app_name = 'messenger'


urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('get_token', UserTokenCreateView.as_view(), name='get_token'),
    path('get_chat_id', UserChat_idView.as_view(), name='chat_id'),
    path('message', MessageView.as_view(), name='message')
]