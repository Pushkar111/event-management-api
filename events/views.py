"""
DRF ViewSets for Event Management System.

Following best practices:
- Use select_related and prefetch_related for query optimization
- Implement filtering, searching, and ordering
- Proper permission classes
- Custom actions for nested resources
- Cache frequently accessed data
"""
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.db.models import Q, Prefetch, Count
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend

from .models import Event, RSVP, Review, UserProfile
from .serializers import (
    EventListSerializer, EventDetailSerializer, EventCreateUpdateSerializer,
    RSVPSerializer, ReviewSerializer, UserProfileSerializer
)
from .permissions import (
    IsOrganizerOrReadOnly, IsInvitedToPrivateEvent,
    IsOwnerOrReadOnly, CanRSVPToEvent
)


class UserProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for UserProfile management.
    Users can only view and update their own profile.
    """
    
    queryset = UserProfile.objects.select_related('user').all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter to show only the current user's profile."""
        return self.queryset.filter(user=self.request.user)

    @action(detail=False, methods=['get', 'put', 'patch'])
    def me(self, request):
        """Get or update current user's profile."""
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        
        if request.method == 'GET':
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        
        serializer = self.get_serializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class EventViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Event management with optimized queries.
    
    Implements:
    - Query optimization with select_related/prefetch_related
    - Filtering by title, location, organizer
    - Search functionality
    - Pagination
    - Custom actions for RSVPs and reviews
    """
    
    permission_classes = [IsAuthenticatedOrReadOnly, IsOrganizerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_public', 'organizer', 'location']
    search_fields = ['title', 'description', 'location']
    ordering_fields = ['start_time', 'created_at', 'title']
    ordering = ['-start_time']

    def get_queryset(self):
        """
        Optimize queries with select_related and prefetch_related.
        Filter private events based on user access.
        """
        queryset = Event.objects.select_related('organizer')

        # If user is not authenticated, show only public events
        if not self.request.user.is_authenticated:
            return queryset.filter(is_public=True)

        # Show public events + private events user is involved with
        user = self.request.user
        queryset = queryset.filter(
            Q(is_public=True) |
            Q(organizer=user) |
            Q(rsvps__user=user)
        ).distinct()

        return queryset

    def get_serializer_class(self):
        """Use different serializers for list and detail views."""
        if self.action == 'list':
            return EventListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return EventCreateUpdateSerializer
        return EventDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve single event with prefetched related data.
        Apply private event access permission.
        """
        instance = self.get_object()
        
        # Check private event access
        if not instance.is_public:
            permission = IsInvitedToPrivateEvent()
            if not permission.has_object_permission(request, self, instance):
                return Response(
                    {'detail': 'You do not have access to this private event.'},
                    status=status.HTTP_403_FORBIDDEN
                )

        # Prefetch related data for detail view
        instance = Event.objects.prefetch_related(
            Prefetch('rsvps', queryset=RSVP.objects.select_related('user')),
            Prefetch('reviews', queryset=Review.objects.select_related('user'))
        ).select_related('organizer').get(pk=instance.pk)

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @method_decorator(cache_page(60 * 5))  # Cache for 5 minutes
    def list(self, request, *args, **kwargs):
        """Cached list view for public events."""
        return super().list(request, *args, **kwargs)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def rsvp(self, request, pk=None):
        """
        RSVP to an event.
        POST /api/events/{id}/rsvp/ with {'status': 'going'|'maybe'|'not_going'}
        """
        event = self.get_object()
        
        # Check if user can RSVP to this event
        can_rsvp = CanRSVPToEvent()
        if not can_rsvp.has_object_permission(request, self, event):
            return Response(
                {'detail': 'You cannot RSVP to this private event.'},
                status=status.HTTP_403_FORBIDDEN
            )

        # Get or create RSVP
        rsvp, created = RSVP.objects.get_or_create(
            event=event,
            user=request.user
        )

        # Update status if provided
        status_value = request.data.get('status', 'going')
        rsvp.status = status_value
        rsvp.save()

        serializer = RSVPSerializer(rsvp)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )

    @action(detail=True, methods=['get'])
    def rsvps(self, request, pk=None):
        """
        List all RSVPs for an event.
        GET /api/events/{id}/rsvps/
        """
        event = self.get_object()
        rsvps = event.rsvps.select_related('user').all()
        serializer = RSVPSerializer(rsvps, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def review(self, request, pk=None):
        """
        Add a review to an event.
        POST /api/events/{id}/review/ with {'rating': 1-5, 'comment': '...'}
        """
        event = self.get_object()

        # Check if review already exists
        existing_review = Review.objects.filter(
            event=event,
            user=request.user
        ).first()

        if existing_review:
            return Response(
                {'detail': 'You have already reviewed this event.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ReviewSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(event=event, user=request.user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        """
        List all reviews for an event.
        GET /api/events/{id}/reviews/
        """
        event = self.get_object()
        reviews = event.reviews.select_related('user').all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)


class RSVPViewSet(viewsets.ModelViewSet):
    """
    ViewSet for RSVP management.
    Users can view all RSVPs but only modify their own.
    """
    
    queryset = RSVP.objects.select_related('user', 'event').all()
    serializer_class = RSVPSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['event', 'status']

    def get_queryset(self):
        """Filter RSVPs for events user has access to."""
        user = self.request.user
        return self.queryset.filter(
            Q(event__is_public=True) |
            Q(event__organizer=user) |
            Q(user=user)
        ).distinct()

    def perform_create(self, serializer):
        """Set user to current user on creation."""
        serializer.save(user=self.request.user)


class ReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Review management.
    Users can view all reviews but only modify their own.
    """
    
    queryset = Review.objects.select_related('user', 'event').all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['event', 'rating']
    ordering_fields = ['rating', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        """Filter reviews for events user has access to."""
        user = self.request.user
        return self.queryset.filter(
            Q(event__is_public=True) |
            Q(event__organizer=user) |
            Q(event__rsvps__user=user)
        ).distinct()

    def perform_create(self, serializer):
        """Set user to current user on creation."""
        serializer.save(user=self.request.user)
