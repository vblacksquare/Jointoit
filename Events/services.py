
from Core.tasks.email import send_email_task
from django.core.cache import cache
from django.contrib.auth import get_user_model

from .models import Event

from config import get_config


CONFIG = get_config()
USER = get_user_model()


class EmailService:

    @staticmethod
    def registered_event(event_member):
        send_email_task.delay(
            account_name="main",
            subject="Registration for event",
            template_name="emails/register_event.html",
            context={
                "username": event_member.user.name,
                "event_name": event_member.event.title,
            },
            to=[event_member.user.email],
        )

    @staticmethod
    def left_event(event_member):
        send_email_task.delay(
            account_name="main",
            subject="Left event",
            template_name="emails/left_event.html",
            context={
                "username": event_member.user.name,
                "event_name": event_member.event.title,
            },
            to=[event_member.user.email],
        )

