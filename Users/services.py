
import random

from Core.tasks.email import send_email_task
from django.core.cache import cache

from config import get_config


CONFIG = get_config()
VERIFICATION_TIMEOUT = 180
RESET_PASSWORD_TIMEOUT = 180



def generate_code():
    return str(random.randint(100000, 999999))


class EmailService:

    @staticmethod
    def verify_email(user):
        key = f"verify:{user.id}"

        if cache.get(key):
            return

        code = generate_code()

        cache.set(key, code, timeout=VERIFICATION_TIMEOUT)

        send_email_task.delay(
            account_name="main",
            subject="Verification",
            template_name="emails/verification.html",
            context={
                "username": user.name,
                "code": code,
            },
            to=[user.email],
        )

    @staticmethod
    def reset_password(user):
        key = f"reset:{user.id}"

        if cache.get(key):
            return

        code = generate_code()

        cache.set(key, code, timeout=RESET_PASSWORD_TIMEOUT)

        send_email_task.delay(
            account_name="main",
            subject="Reset Password",
            template_name="emails/reset_password.html",
            context={
                "username": user.name,
                "code": code,
            },
            to=[user.email],
        )
