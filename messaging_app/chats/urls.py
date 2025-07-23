# messaging_app/chats/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConversationViewSet, MessageViewSet

router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'conversations/(?P<conversation_id>\d+)/messages', MessageViewSet, basename='message')

urlpatterns = [
    path('', include(router.urls)),
]
