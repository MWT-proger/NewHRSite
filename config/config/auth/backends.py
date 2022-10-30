from django.contrib.auth.backends import ModelBackend, UserModel


class EmailModelBackend(ModelBackend):

    def authenticate(self, request, email=None, password=None, **kwargs):
        if email is None or password is None:
            return

        try:
            user = UserModel._default_manager.get(email=email)
        except UserModel.DoesNotExist:
            UserModel().set_password(password)

        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
