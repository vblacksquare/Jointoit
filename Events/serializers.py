from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Event, EventMember


User = get_user_model()


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ["id", "title", "description", "date", "location", "organizer"]
        read_only_fields = ("organizer", "search_vector")


class EventMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventMember
        fields = "__all__"


class RegisterEventView(serializers.Serializer):
    event = Event()


class KickMemberSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()


class SearchEventsSerializer(serializers.Serializer):
    query = serializers.CharField()

    organizer_id = serializers.IntegerField(
        required=False
    )

    date_from = serializers.DateTimeField(
        required=False
    )

    date_to = serializers.DateTimeField(
        required=False
    )

    page = serializers.IntegerField(
        required=False
    )
