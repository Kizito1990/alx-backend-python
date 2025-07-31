

from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.shortcuts import render
from .models import Message
from django.views import View

@cache_page(60)  # Caches the view for 60 seconds
def message_list(request):
    messages = Message.objects.all().select_related('sender', 'receiver').order_by('-timestamp')
    return render(request, 'chats/message_list.html', {'messages': messages})


@method_decorator(cache_page(60), name='dispatch')
class MessageListView(View):
    def get(self, request, *args, **kwargs):
        messages = Message.objects.all().select_related('sender', 'receiver').order_by('-timestamp')
        return render(request, 'chats/message_list.html', {'messages': messages})

