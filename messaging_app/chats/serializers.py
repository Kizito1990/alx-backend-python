

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Conversation, Message
from rest_framework.exceptions import ValidationError

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    short_content = serializers.CharField(source='content', max_length=50, read_only=True)
    message_length = serializers.SerializerMethodField()

    # SerializerMethodField to calculate the length of the message
    def get_message_length(self, obj):
        return len(obj.content)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'content', 'short_content', 'message_length', 'timestamp']

    # Custom validation for content field (e.g. no empty content)
    def validate_content(self, value):
        if not value.strip():
            raise ValidationError("Message content cannot be empty.")
        return value


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    total_messages = serializers.SerializerMethodField()

    # SerializerMethodField to return the number of messages in a conversation
    def get_total_messages(self, obj):
        return obj.messages.count()

    # Custom validation for participants: at least 2 participants in a conversation
    def validate_participants(self, value):
        if len(value) < 2:
            raise ValidationError("A conversation must have at least two participants.")
        return value

    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'created_at', 'messages', 'total_messages']

