from django.urls import path, include
from rest_framework import routers
from .views import ConversationViewSet, MessageViewSet
from rest_framework_nested.routers import NestedDefaultRouter

router = routers.DefaultRouter()
router = NestedDefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')


# Nested router for messages under conversations
conversations_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversations_router.register(r'messages', MessageViewSet, basename='conversation-messages')

urlpatterns = [
    path('', include(router.urls)),
]
