from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six
class TokenGenerator(PasswordResetTokenGenerator):
    def make_token(self, user, timestamp):
        return(six.text_type(user.pk)+six.text_type(timestamp)+six.text_type(user.is_active))

token_generator = TokenGenerator()