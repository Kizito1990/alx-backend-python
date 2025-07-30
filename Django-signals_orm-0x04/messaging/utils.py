# messaging/utils.py

def get_threaded_conversation(message):
    """
    Recursively fetch all replies to a given message.
    """
    conversation = {
        'id': message.id,
        'content': message.content,
        'sender': message.sender.username,
        'timestamp': message.timestamp,
        'replies': []
    }
    for reply in message.replies.all().select_related('sender'):
        conversation['replies'].append(get_threaded_conversation(reply))
    return conversation
