from rest_framework import permissions
from .models import Conversation

class IsParticipantOrSender(permissions.BasePermission):
    """
    Custom permission to only allow participants to view conversations and messages.
    """

    def has_object_permission(self, request, view, obj):
        # For conversations
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()
        # For messages
        if hasattr(obj, 'sender'):
            return obj.sender == request.user or request.user in obj.conversation.participants.all()
        return False
class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation
    to view or modify messages in that conversation.
    """

    def has_permission(self, request, view):
        # User must be authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Check if the user is a participant in the conversation.
        This method is used for object-level permissions.
        """
        if hasattr(obj, 'conversation'):
            return request.user in obj.conversation.participants.all()
        elif hasattr(obj, 'participants'):
            return request.user in obj.participants.all()
        return False
