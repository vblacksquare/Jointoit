import string
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class PasswordValidator:
    def validate(self, password, user=None):
        has_letter = any(char.isalpha() for char in password)
        has_num_or_spec = any(
            char.isdigit() or char in string.punctuation
            for char in password
        )

        if not (has_letter and has_num_or_spec):
            raise ValidationError(
                _("Password must contain at least 1 number or special character."),
                code='password_too_simple',
            )
