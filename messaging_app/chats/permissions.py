from rest_framework import permissions

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
