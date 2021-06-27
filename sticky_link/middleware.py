from django.contrib.auth import authenticate, login
from sticky_link import env


def login_debug_user(get_response):
    def middleware(request):
        user = authenticate(request, username=env.DEBUG_USER_USERNAME, password=env.DEBUG_USER_PASSWORD)
        if user is not None:
            login(request, user)
        response = get_response(request)
        return response

    return middleware
