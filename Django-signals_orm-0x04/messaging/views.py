
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .utils import get_threaded_conversation

@csrf_exempt
@login_required
def delete_user(request):
    if request.method == 'POST':
        user = request.user
        username = user.username
        user.delete()
        return JsonResponse({'message': f'User {username} deleted successfully.'})
    else:
        return JsonResponse({'error': 'Only POST requests allowed.'}, status=405)

def threaded_conversation_view(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    conversation = get_threaded_conversation(message)
    return JsonResponse(conversation, safe=False)
