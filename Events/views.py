
from django.contrib.postgres.search import (
    SearchQuery,
    SearchRank,
    TrigramSimilarity
)
from django.core.cache import cache
import hashlib
import json
from django.db.models import Q
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiResponse
from rest_framework.decorators import action
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from .permissions import IsOrganizerOrReadOnly, IsOrganizer
from .models import Event, EventMember
from .serializers import EventSerializer, EventMemberSerializer, SearchEventsSerializer, KickMemberSerializer


@extend_schema_view(
    list=extend_schema(
        summary="List events",
        tags=["Event Organizer"],
    ),
    retrieve=extend_schema(
        summary="Get event detail",
        tags=["Event Organizer"],
    ),
    create=extend_schema(
        summary="Create event",
        tags=["Event Organizer"],
    ),
    update=extend_schema(
        summary="Update event",
        tags=["Event Organizer"],
    ),
    partial_update=extend_schema(
        summary="Partial update event",
        tags=["Event Organizer"],
    ),
    destroy=extend_schema(
        summary="Delete event",
        tags=["Event Organizer"],
    ),
)
class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated, IsOrganizerOrReadOnly]

    def get_queryset(self):
        if self.action == 'list':
            return Event.objects.filter(organizer=self.request.user)
        return Event.objects.all()

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

    @extend_schema(
        summary="Register current user for an event",
        tags=["Event Public"],
        responses={
            200: OpenApiResponse(description="Registered for an event")
        },
    )
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def register(self, request, pk=None):
        event = self.get_object()

        member, created = EventMember.objects.get_or_create(
            event=event,
            user=request.user
        )

        if not created:
            return Response({"error": "Already registered"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": f"Registered for {event.id}"}, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Leave current user from event",
        tags=["Event Public"],
        responses={
            200: OpenApiResponse(description="Leave from event")
        },
    )
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def leave(self, request, pk=None):
        event = self.get_object()

        member = EventMember.objects.filter(event=event, user=request.user).first()

        if not member:
            return Response({"error": "You are not member of event"}, status=status.HTTP_400_BAD_REQUEST)

        member.delete()

        return Response({"message": f"Left from event"}, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Event members",
        tags=["Event Organizer"],
        responses={
            200: OpenApiResponse(description="Members list")
        },
    )
    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated, IsOrganizer])
    def members(self, request, pk=None):
        event = self.get_object()

        members = EventMember.objects.filter(event=event)

        serializer = EventMemberSerializer(members, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Kick Member",
        tags=["Event Organizer"],
        request=KickMemberSerializer,
        responses={
            200: OpenApiResponse(description="Members list")
        },
    )
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, IsOrganizer])
    def kick(self, request, pk=None):
        event = self.get_object()

        serializer = KickMemberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = serializer.validated_data["user_id"]
        member = EventMember.objects.filter(
            event=event,
            user_id=user_id
        ).first()

        if not member:
            return Response({"error": "User is not member of event"}, status=status.HTTP_400_BAD_REQUEST)

        member.delete()

        return Response({"message": f"Kicked member"}, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Search Events",
        tags=["Event Public"],
        request=SearchEventsSerializer,
        responses={
            200: OpenApiResponse(description="Events list"),
        },
    )
    @action(
        detail=False,
        methods=["post"],
        permission_classes=[permissions.IsAuthenticated],
    )
    def search(self, request):

        serializer = SearchEventsSerializer(
            data=request.query_params
        )

        serializer.is_valid(
            raise_exception=True
        )

        validated_data = serializer.validated_data

        query_text = validated_data["query"]

        organizer_id = validated_data.get(
            "organizer_id"
        )

        date_from = validated_data.get(
            "date_from"
        )

        date_to = validated_data.get(
            "date_to"
        )

        cache_key_raw = {
            "query": query_text,
            "organizer_id": organizer_id,
            "date_from": str(date_from),
            "date_to": str(date_to),
        }

        cache_key = "event_search:" + hashlib.md5(
            json.dumps(cache_key_raw, sort_keys=True).encode()
        ).hexdigest()

        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)

        query = SearchQuery(
            query_text,
            config="simple",
        )

        queryset = (
            Event.objects
            .select_related("organizer")
            .annotate(
                rank=SearchRank(
                    "search_vector",
                    query,
                ),

                similarity=(
                    TrigramSimilarity(
                        "title",
                        query_text,
                    ) * 2 +
                    TrigramSimilarity(
                        "description",
                        query_text,
                    )
                )
            )
            .filter(
                Q(rank__gte=0.05) |
                Q(similarity__gt=0.1)
            )
        )

        if organizer_id:
            queryset = queryset.filter(
                organizer_id=organizer_id
            )

        if date_from:
            queryset = queryset.filter(
                date__gte=date_from
            )

        if date_to:
            queryset = queryset.filter(
                date__lte=date_to
            )

        queryset = queryset.order_by(
            "-rank",
            "-similarity",
            "-date",
        )

        serializer = EventSerializer(
            queryset,
            many=True,
        )

        cache.set(cache_key, serializer.data, timeout=60 * 5)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
