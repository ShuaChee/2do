from django.conf import settings
from django.shortcuts import redirect
from .models import MySession


def session_check(session_id):
    try:
        MySession.objects.get(session_id=session_id)
        return True
    except MySession.DoesNotExist:
        return False


class MyAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.path in ['/login/', '/logout/'] or request.path.startswith('/admin/'):
            return response
        session_id = request.COOKIES.get(settings.MY_SESSION_ID)
        if session_id and session_check(session_id):
            return response
        else:
            return redirect('login')
