
from celery import shared_task
from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string

from config import get_config

import logging


logger = logging.getLogger(__name__)


CONFIG = get_config()
EMAILS = {
    email.name: email
    for email in CONFIG.emails
}


@shared_task(bind=True, max_retries=3)
def send_email_task(
    self,
    account_name: str,
    subject: str,
    template_name: str,
    context: dict,
    to: list[str],
):
    try:
        cfg = EMAILS[account_name]

        connection = get_connection(
            host=cfg.host,
            port=cfg.port,
            username=cfg.user,
            password=cfg.password,
            use_tls=cfg.use_tls,
            use_ssl=cfg.use_ssl
        )

        html_body = render_to_string(template_name, context)

        email = EmailMultiAlternatives(
            subject=subject,
            body=html_body,
            from_email=cfg.user,
            to=to,
            connection=connection,
        )

        email.attach_alternative(html_body, "text/html")
        email.send()

        logger.info(f"Sending email '{template_name}': {account_name}-{cfg.user} -> {to}")

    except Exception as exc:
        raise self.retry(exc=exc, countdown=30)
