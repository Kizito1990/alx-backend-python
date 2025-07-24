

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOrSender
from .permissions import IsParticipantOfConversation


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['participants']  # You can filter by participants' user ID
    permission_classes = [IsParticipantOrSender]
    permission_classes = [IsParticipantOfConversation]

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user).distinct()

    def create(self, request, *args, **kwargs):
        participants = request.data.get('participants', [])
        if request.user.id not in participants:
            participants.append(request.user.id)

        serializer = self.get_serializer(data={'participants': participants})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['conversation', 'sender']
    permission_classes = [IsParticipantOrSender]
    permission_classes = [IsParticipantOfConversation]

    def get_queryset(self):
        return Message.objects.filter(
            conversation__participants=self.request.user
        
    
    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
