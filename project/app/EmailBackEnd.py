from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class EmailBackEnd(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        # Use the custom user model
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)  # Using email instead of username
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):  # Verify the password
                return user
        return None