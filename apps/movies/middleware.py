from apps.movies.models import UserToken
from django.contrib.auth import logout
from django.shortcuts import redirect


class LoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            if request.META.get('HTTP_AUTHORIZATION'):
                token = request.META.get('HTTP_AUTHORIZATION')
                token = UserToken.objects.get(token=token)
                request.user = token.user
            if not request.user.is_anonymous:
                UserToken.objects.get(user=request.user)
        except Exception:
            logout(request)
            response = redirect('logout')
            response.delete_cookie('user_location')
            return response

        response = self.get_response(request)
        return response
