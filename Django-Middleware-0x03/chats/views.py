

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOrSender
from .permissions import IsParticipantOfConversation
from .pagination import MessagePagination
from .filters import MessageFilter


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

    pagination_class = MessagePagination

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = MessageFilter
    ordering_fields = ['timestamp']
    ordering = ['-timestamp']

    def get_queryset(self):
        return Message.objects.filter(conversation__participants=self.request.user)

    def perform_create(self, serializer):
        conversation_id = self.request.data.get("conversation")
        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            raise PermissionDenied(detail="Conversation does not exist", code=HTTP_403_FORBIDDEN)

        if self.request.user not in conversation.participants.all():
            raise PermissionDenied(detail="You are not a participant of this conversation", code=HTTP_403_FORBIDDEN)

        serializer.save(sender=self.request.user)