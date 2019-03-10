from django.conf import settings
from todolist.models import MySession


class UserNotAuthorized(Exception):
    pass


def session_check(session_id):
    try:
        MySession.objects.get(session_id=session_id)
        return True
    except MySession.DoesNotExist:
        return False


def get_user(request):
    session_id = request.COOKIES[settings.MY_SESSION_ID]
    try:
        session = MySession.objects.get(session_id=session_id)
    except MySession.DoesNotExist:
        raise UserNotAuthorized()

    return session.user
