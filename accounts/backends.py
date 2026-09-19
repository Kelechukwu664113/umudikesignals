from django.contrib.auth.backends import ModelBackend
from .models import User, normalize_phone_number


class PhoneNumberBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            return None
        normalized = normalize_phone_number(username)
        try:
            user = User.objects.get(phone_number=normalized)
        except User.DoesNotExist:
            return None
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None