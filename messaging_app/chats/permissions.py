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
    def has_permission(self, request, view):
        # Allow only authenticated users
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Allow safe methods if the user is a participant
        if request.method in SAFE_METHODS:
            return request.user in obj.conversation.participants.all()

        # Allow PUT, PATCH, DELETE only if user is a participant
        if request.method in ["PUT", "PATCH", "DELETE"]:
            return request.user in obj.conversation.participants.all()

        return False
