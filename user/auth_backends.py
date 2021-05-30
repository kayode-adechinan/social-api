from user import models
from django.contrib.auth.hashers import check_password


class EmailAuthBackend(object):
    def authenticate(self, request, username=None, password=None):
        try:
      # Check if the user exists in Django's database
            user = models.User.objects.get(email=username)
        except models.User.DoesNotExist:
            return None

    # Check password of the user we found
        if check_password(password, user.password):
            return user
        return None
    # Required for your backend to work properly - unchanged in most scenarios
    def get_user(self, user_id):
        try:
            return models.User.objects.get(pk=user_id)
        except models.User.DoesNotExist:
            return None


class PhoneAuthBackend(object):
    def authenticate(self, request, username=None, password=None):
        try:
      # Check if the user exists in Django's database
            user = models.User.objects.get(phone=username)
        except models.User.DoesNotExist:
            return None

    # Check password of the user we found
        if check_password(password, user.password):
            return user
        return None
    # Required for your backend to work properly - unchanged in most scenarios
    def get_user(self, user_id):
        try:
            return models.User.objects.get(pk=user_id)
        except models.User.DoesNotExist:
            return None
