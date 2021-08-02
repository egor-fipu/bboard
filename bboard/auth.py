from django.contrib.auth.backends import ModelBackend

from main.models import AdvUser


class EmailAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None):
        if '@' in username:
            kwargs = {'email': username}
        else:
            kwargs = {'username': username}

        try:
            user = AdvUser.objects.get(**kwargs)
            if user.check_password(password):
                return user
            else:
                return None
        except AdvUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return AdvUser.objects.get(pk=user_id)
        except AdvUser.DoesNotExist:
            return None
