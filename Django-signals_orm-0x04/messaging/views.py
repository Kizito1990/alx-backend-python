
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

@login_required
def send_message(request):
    if request.method == 'POST':
        receiver_id = request.POST.get('receiver_id')
        content = request.POST.get('content')

        if not receiver_id or not content:
            return render(request, 'messaging/send_message.html', {
                'error': 'Receiver and content are required.'
            })

        receiver = get_object_or_404(User, id=receiver_id)

        Message.objects.create(
            sender=request.user,       # ✅ Sender is the logged-in user
            receiver=receiver,         # ✅ Receiver is selected by the sender
            content=content
        )

        return redirect('inbox')  # redirect to any message list view
    else:
        users = User.objects.exclude(id=request.user.id)
        return render(request, 'messaging/send_message.html', {'users': users})
        
@login_required
def inbox(request):
    # Fetch messages where the current user is the receiver
    messages = Message.objects.filter(receiver=request.user)\
                              .select_related('sender', 'receiver')\
                              .order_by('-timestamp')

    return render(request, 'messaging/inbox.html', {'messages': messages})