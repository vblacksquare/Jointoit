from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import EventMember
from .services import EmailService


@receiver(post_save, sender=EventMember)
def create_member(sender, instance, created, **kwargs):
    if created:
        EmailService.registered_event(instance)


@receiver(post_delete, sender=EventMember)
def after_delete_memer(sender, instance, **kwargs):
    EmailService.left_event(instance)
