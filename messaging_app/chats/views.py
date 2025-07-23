

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from rest_framework.exceptions import ValidationError

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    # List conversations for the current user (filtering by participants)
    def get_queryset(self):
        user = self.request.user
        return Conversation.objects.filter(participants=user)

    # Create a new conversation (ensuring that at least 2 participants are specified)
    def create(self, request, *args, **kwargs):
        participants = request.data.get('participants', [])
        if len(participants) < 2:
            raise ValidationError("A conversation must have at least two participants.")
        
        # Ensure the current user is included in the participants
        if request.user.id not in participants:
            participants.append(request.user.id)

        request.data['participants'] = participants
        return super().create(request, *args, **kwargs)

    # Custom action to add a participant to an existing conversation
    @action(detail=True, methods=['post'])
    def add_participant(self, request, pk=None):
        conversation = self.get_object()
        user_id = request.data.get('user_id')
        
        if not user_id:
            raise ValidationError("User ID is required to add a participant.")
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise ValidationError("User not found.")
        
        if user in conversation.participants.all():
            raise ValidationError("User is already a participant.")
        
        conversation.participants.add(user)
        conversation.save()
        return Response({"detail": "User added to conversation."}, status=status.HTTP_200_OK)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    # Filter messages by conversation
    def get_queryset(self):
        conversation_id = self.kwargs.get('conversation_id')
        return Message.objects.filter(conversation_id=conversation_id)

    # Create a new message in an existing conversation
    def create(self, request, *args, **kwargs):
        conversation_id = self.kwargs.get('conversation_id')
        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            raise ValidationError("Conversation not found.")

        # Ensure the user is a participant in the conversation
        if request.user not in conversation.participants.all():
            raise ValidationError("You must be a participant in the conversation to send a message.")
        
        request.data['conversation'] = conversation.id
        request.data['sender'] = request.user.id
        return super().create(request, *args, **kwargs)

    # Custom action to send a message to the conversation
    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        conversation_id = self.kwargs.get('conversation_id')
        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            raise ValidationError("Conversation not found.")

        # Ensure the user is a participant in the conversation
        if request.user not in conversation.participants.all():
            raise ValidationError("You must be a participant in the conversation to send a message.")

        content = request.data.get('content')
        if not content:
            raise ValidationError("Message content cannot be empty.")

        message = Message.objects.create(
            conversation=conversation,
            sender=request.user,
            content=content
        )

        # Respond with the newly created message
        message_serializer = MessageSerializer(message)
        return Response(message_serializer.data, status=status.HTTP_201_CREATED)
