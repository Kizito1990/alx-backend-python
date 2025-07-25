import time
from django.http import JsonResponse
from collections import defaultdict

import logging
from datetime import datetime
from django.http import HttpResponseForbidden
import logging
from datetime import datetime
from django.utils.deprecation import MiddlewareMixin

# Configure logger
logger = logging.getLogger(__name__)
handler = logging.FileHandler('requests.log')  # This will create `requests.log` in your root directory
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


class RequestLoggingMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(log_message)

        response = self.get_response(request)
        return response


class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.offensive_words = {"badword1", "badword2", "stupid", "idiot"}  # Add more as needed

    def __call__(self, request):
        if request.method == "POST" and request.path.startswith("/messages/"):
            try:
                data = json.loads(request.body.decode('utf-8'))
                message = data.get("message", "")

                if any(word.lower() in message.lower() for word in self.offensive_words):
                    return JsonResponse(
                        {"error": "Offensive language detected. Please revise your message."},
                        status=400
                    )
            except (ValueError, json.JSONDecodeError):
                pass  # ignore malformed JSON and let normal error handling take over

        return self.get_response(request)

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_time = datetime.now().time()
        start_time = time(18, 0)  # 6:00 PM
        end_time = time(21, 0)    # 9:00 PM

        # Block access if current time is NOT between 6PM and 9PM
        if not (start_time <= current_time <= end_time):
            return HttpResponseForbidden("Access to this app is only allowed between 6 PM and 9 PM.")

        return self.get_response(request)
    
class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Define restricted HTTP methods
        restricted_methods = ['POST', 'PUT', 'PATCH', 'DELETE']

        # Only check role if user is making a restricted request
        if request.method in restricted_methods:
            user = request.user

            if not user.is_authenticated:
                return JsonResponse({'error': 'Authentication required.'}, status=403)

            # Assuming the User model has a 'role' attribute
            if not hasattr(user, 'role') or user.role not in ['admin', 'moderator']:
                return JsonResponse({'error': 'Permission denied. Admin or moderator role required.'}, status=403)

        return self.get_response(request)

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.offensive_words = {"badword1", "badword2", "stupid", "idiot"}  # Add more as needed

    def __call__(self, request):
        if request.method == "POST" and request.path.startswith("/messages/"):
            try:
                data = json.loads(request.body.decode('utf-8'))
                message = data.get("message", "")

                if any(word.lower() in message.lower() for word in self.offensive_words):
                    return JsonResponse(
                        {"error": "Offensive language detected. Please revise your message."},
                        status=400
                    )
            except (ValueError, json.JSONDecodeError):
                pass  # ignore malformed JSON and let normal error handling take over

        return self.get_response(request)

