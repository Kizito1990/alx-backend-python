import time
from django.http import JsonResponse
from collections import defaultdict

import logging
from datetime import datetime
from django.http import HttpResponseForbidden

# Configure logger
logger = logging.getLogger(__name__)
handler = logging.FileHandler('requests.log')  # This will create `requests.log` in your root directory
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(log_message)

        response = self.get_response(request)
        return response

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



class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.message_logs = defaultdict(list)  # IP -> list of timestamps

        # Rate limit settings
        self.max_messages = 5
        self.time_window = 60  # seconds (1 minute)

    def __call__(self, request):
        # Only rate limit POST requests to /messages/ endpoint
        if request.method == "POST" and request.path.startswith("/messages/"):
            ip = self.get_client_ip(request)
            now = time.time()
            window_start = now - self.time_window

            # Clean old requests
            self.message_logs[ip] = [t for t in self.message_logs[ip] if t > window_start]

            if len(self.message_logs[ip]) >= self.max_messages:
                return JsonResponse(
                    {"error": "Rate limit exceeded. Only 5 messages per minute allowed."},
                    status=429
                )

            self.message_logs[ip].append(now)

        return self.get_response(request)

    def get_client_ip(self, request):
        """Get IP address from request headers or fallback to remote address."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
