from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='chat_sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='chat_receiver', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)  # New field

    def __str__(self):
        return f"{self.sender.username} to {self.receiver.username}: {self.content[:30]}"

class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='history')
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History for message ID {self.message.id} at {self.edited_at}"
