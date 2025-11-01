"""
DRF Serializers for Event Management System.

Following best practices:
- Separate serializers for read and write operations where needed
- Nested serializers for related data
- Custom validation methods
- Read-only fields for computed properties
- Proper error messages
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from django.utils import timezone
from .models import UserProfile, Event, RSVP, Review


class UserSerializer(serializers.ModelSerializer):
    """Basic user serializer for nested representations."""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for UserProfile with nested user data."""
    
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = UserProfile
        fields = [
            'id', 'user', 'username', 'email', 'full_name',
            'bio', 'location', 'profile_picture',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class RSVPSerializer(serializers.ModelSerializer):
    """Serializer for RSVP with user details."""
    
    user_username = serializers.CharField(source='user.username', read_only=True)
    event_title = serializers.CharField(source='event.title', read_only=True)
    
    class Meta:
        model = RSVP
        fields = [
            'id', 'event', 'user', 'user_username',
            'event_title', 'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def validate(self, data):
        """Ensure user can't RSVP to private events they're not invited to."""
        request = self.context.get('request')
        event = data.get('event')
        
        if event and not event.is_public:
            # Check if user is organizer or already has RSVP
            if event.organizer != request.user:
                # In a real app, you'd check an invitations table here
                # For now, we'll allow if user already has an RSVP
                existing_rsvp = RSVP.objects.filter(
                    event=event,
                    user=request.user
                ).first()
                if not existing_rsvp and self.instance is None:
                    raise serializers.ValidationError(
                        "You cannot RSVP to private events you're not invited to."
                    )
        
        return data


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for Review with user details."""
    
    user_username = serializers.CharField(source='user.username', read_only=True)
    event_title = serializers.CharField(source='event.title', read_only=True)
    
    class Meta:
        model = Review
        fields = [
            'id', 'event', 'user', 'user_username',
            'event_title', 'rating', 'comment',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def validate_rating(self, value):
        """Validate rating is between 1 and 5."""
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    def validate(self, data):
        """Ensure user attended the event before reviewing."""
        request = self.context.get('request')
        event = data.get('event')
        
        # Check if user has RSVP'd with 'going' status
        if event:
            rsvp = RSVP.objects.filter(
                event=event,
                user=request.user,
                status='going'
            ).first()
            
            if not rsvp:
                raise serializers.ValidationError(
                    "You can only review events you've RSVP'd as 'Going'."
                )
        
        return data


class EventListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for event listings.
    Uses select_related optimization for organizer.
    """
    
    organizer_username = serializers.CharField(source='organizer.username', read_only=True)
    attendee_count = serializers.IntegerField(read_only=True)
    is_upcoming = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Event
        fields = [
            'id', 'title', 'location', 'start_time', 'end_time',
            'is_public', 'organizer', 'organizer_username',
            'attendee_count', 'is_upcoming', 'created_at'
        ]
        read_only_fields = ['id', 'organizer', 'created_at']


class EventDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for single event view.
    Includes nested RSVPs and reviews with prefetch optimization.
    """
    
    organizer = UserSerializer(read_only=True)
    rsvps = RSVPSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    attendee_count = serializers.IntegerField(read_only=True)
    is_upcoming = serializers.BooleanField(read_only=True)
    is_ongoing = serializers.BooleanField(read_only=True)
    average_rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'location',
            'start_time', 'end_time', 'is_public',
            'organizer', 'attendee_count', 'is_upcoming',
            'is_ongoing', 'average_rating', 'rsvps', 'reviews',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'organizer', 'created_at', 'updated_at']

    def get_average_rating(self, obj):
        """Calculate average rating from reviews."""
        reviews = obj.reviews.all()
        if reviews:
            total = sum(review.rating for review in reviews)
            return round(total / len(reviews), 2)
        return None


class EventCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating events.
    Separate from detail serializer to avoid nested complexity.
    """
    
    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'location',
            'start_time', 'end_time', 'is_public',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, data):
        """Validate event dates."""
        start_time = data.get('start_time', getattr(self.instance, 'start_time', None))
        end_time = data.get('end_time', getattr(self.instance, 'end_time', None))
        
        if start_time and end_time:
            if end_time <= start_time:
                raise serializers.ValidationError({
                    'end_time': 'End time must be after start time.'
                })
        
        # Validate start time is in the future for new events
        if not self.instance and start_time:
            if start_time < timezone.now():
                raise serializers.ValidationError({
                    'start_time': 'Cannot create events with past start times.'
                })
        
        return data

    def create(self, validated_data):
        """Set organizer to current user on creation."""
        request = self.context.get('request')
        validated_data['organizer'] = request.user
        return super().create(validated_data)
