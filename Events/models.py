
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex


User = get_user_model()


class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, max_length=1500)

    date = models.DateTimeField()

    location = models.TextField(max_length=1500)

    organizer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="organized_events"
    )

    search_vector = SearchVectorField(null=True)

    class Meta:
        indexes = [
            GinIndex(fields=["search_vector"]),
        ]


class EventMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
