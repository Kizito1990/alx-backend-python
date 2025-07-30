
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

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
