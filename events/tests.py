"""
Comprehensive tests for Event Management System.

Testing:
- Models and business logic
- Serializers and validation
- API endpoints
- Permissions
- Query optimization

Run with: pytest
or: python manage.py test
"""
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from events.models import Event, RSVP, Review, UserProfile
from events.serializers import EventDetailSerializer, RSVPSerializer, ReviewSerializer


class UserProfileModelTest(TestCase):
    """Test UserProfile model."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_create_profile(self):
        """Test creating a user profile."""
        profile = UserProfile.objects.create(
            user=self.user,
            full_name='Test User',
            bio='Test bio',
            location='Test City'
        )
        self.assertEqual(str(profile), "testuser's Profile")
        self.assertEqual(profile.display_name, 'Test User')

    def test_display_name_fallback(self):
        """Test display_name falls back to username."""
        profile = UserProfile.objects.create(user=self.user)
        self.assertEqual(profile.display_name, 'testuser')


class EventModelTest(TestCase):
    """Test Event model and business logic."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='organizer',
            email='organizer@example.com',
            password='testpass123'
        )
        self.start_time = timezone.now() + timedelta(days=1)
        self.end_time = self.start_time + timedelta(hours=2)

    def test_create_event(self):
        """Test creating an event."""
        event = Event.objects.create(
            title='Test Event',
            description='Test description',
            organizer=self.user,
            location='Test Location',
            start_time=self.start_time,
            end_time=self.end_time,
            is_public=True
        )
        self.assertEqual(str(event), 'Test Event by organizer')
        self.assertTrue(event.is_upcoming)
        self.assertFalse(event.is_ongoing)

    def test_event_validation_end_before_start(self):
        """Test that event validation prevents end_time before start_time."""
        from django.core.exceptions import ValidationError
        
        with self.assertRaises(ValidationError):
            event = Event(
                title='Test Event',
                description='Test description',
                organizer=self.user,
                location='Test Location',
                start_time=self.start_time,
                end_time=self.start_time - timedelta(hours=1),
                is_public=True
            )
            event.save()

    def test_attendee_count(self):
        """Test attendee count property."""
        event = Event.objects.create(
            title='Test Event',
            description='Test description',
            organizer=self.user,
            location='Test Location',
            start_time=self.start_time,
            end_time=self.end_time,
            is_public=True
        )
        
        user2 = User.objects.create_user(username='user2', password='test123')
        user3 = User.objects.create_user(username='user3', password='test123')
        
        RSVP.objects.create(event=event, user=user2, status='going')
        RSVP.objects.create(event=event, user=user3, status='maybe')
        
        self.assertEqual(event.attendee_count, 1)  # Only 'going' status


class RSVPModelTest(TestCase):
    """Test RSVP model."""

    def setUp(self):
        self.organizer = User.objects.create_user(username='organizer', password='test123')
        self.user = User.objects.create_user(username='attendee', password='test123')
        self.event = Event.objects.create(
            title='Test Event',
            description='Test description',
            organizer=self.organizer,
            location='Test Location',
            start_time=timezone.now() + timedelta(days=1),
            end_time=timezone.now() + timedelta(days=1, hours=2),
            is_public=True
        )

    def test_create_rsvp(self):
        """Test creating an RSVP."""
        rsvp = RSVP.objects.create(
            event=self.event,
            user=self.user,
            status='going'
        )
        self.assertEqual(str(rsvp), f'attendee - Test Event (Going)')

    def test_rsvp_unique_constraint(self):
        """Test that a user can only have one RSVP per event."""
        from django.db import IntegrityError
        
        RSVP.objects.create(event=self.event, user=self.user, status='going')
        
        with self.assertRaises(IntegrityError):
            RSVP.objects.create(event=self.event, user=self.user, status='maybe')


class ReviewModelTest(TestCase):
    """Test Review model."""

    def setUp(self):
        self.organizer = User.objects.create_user(username='organizer', password='test123')
        self.user = User.objects.create_user(username='reviewer', password='test123')
        self.event = Event.objects.create(
            title='Test Event',
            description='Test description',
            organizer=self.organizer,
            location='Test Location',
            start_time=timezone.now() + timedelta(days=1),
            end_time=timezone.now() + timedelta(days=1, hours=2),
            is_public=True
        )

    def test_create_review(self):
        """Test creating a review."""
        review = Review.objects.create(
            event=self.event,
            user=self.user,
            rating=5,
            comment='Great event!'
        )
        self.assertEqual(str(review), 'reviewer - Test Event (5/5)')

    def test_review_rating_validation(self):
        """Test that review rating must be between 1 and 5."""
        from django.core.exceptions import ValidationError
        
        with self.assertRaises(ValidationError):
            review = Review(
                event=self.event,
                user=self.user,
                rating=6,
                comment='Too high'
            )
            review.save()


class EventAPITest(APITestCase):
    """Test Event API endpoints."""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            password='testpass123'
        )
        self.start_time = timezone.now() + timedelta(days=1)
        self.end_time = self.start_time + timedelta(hours=2)

    def test_list_events_unauthenticated(self):
        """Test listing public events without authentication."""
        Event.objects.create(
            title='Public Event',
            description='Test',
            organizer=self.user,
            location='Test Location',
            start_time=self.start_time,
            end_time=self.end_time,
            is_public=True
        )
        
        response = self.client.get('/api/events/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_create_event_authenticated(self):
        """Test creating an event with authentication."""
        self.client.force_authenticate(user=self.user)
        
        data = {
            'title': 'New Event',
            'description': 'Test event',
            'location': 'Test Location',
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat(),
            'is_public': True
        }
        
        response = self.client.post('/api/events/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Event')

    def test_create_event_unauthenticated(self):
        """Test that unauthenticated users cannot create events."""
        data = {
            'title': 'New Event',
            'description': 'Test event',
            'location': 'Test Location',
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat(),
            'is_public': True
        }
        
        response = self.client.post('/api/events/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_event_by_organizer(self):
        """Test that organizers can update their events."""
        event = Event.objects.create(
            title='Original Title',
            description='Test',
            organizer=self.user,
            location='Test Location',
            start_time=self.start_time,
            end_time=self.end_time,
            is_public=True
        )
        
        self.client.force_authenticate(user=self.user)
        
        data = {'title': 'Updated Title'}
        response = self.client.patch(f'/api/events/{event.id}/', data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Title')

    def test_update_event_by_non_organizer(self):
        """Test that non-organizers cannot update events."""
        event = Event.objects.create(
            title='Original Title',
            description='Test',
            organizer=self.user,
            location='Test Location',
            start_time=self.start_time,
            end_time=self.end_time,
            is_public=True
        )
        
        self.client.force_authenticate(user=self.other_user)
        
        data = {'title': 'Hacked Title'}
        response = self.client.patch(f'/api/events/{event.id}/', data)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_event_by_organizer(self):
        """Test that organizers can delete their events."""
        event = Event.objects.create(
            title='Event to Delete',
            description='Test',
            organizer=self.user,
            location='Test Location',
            start_time=self.start_time,
            end_time=self.end_time,
            is_public=True
        )
        
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/api/events/{event.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Event.objects.filter(id=event.id).exists())

    def test_rsvp_to_public_event(self):
        """Test RSVPing to a public event."""
        event = Event.objects.create(
            title='Public Event',
            description='Test',
            organizer=self.user,
            location='Test Location',
            start_time=self.start_time,
            end_time=self.end_time,
            is_public=True
        )
        
        self.client.force_authenticate(user=self.other_user)
        
        data = {'status': 'going'}
        response = self.client.post(f'/api/events/{event.id}/rsvp/', data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'going')

    def test_add_review_to_event(self):
        """Test adding a review to an event."""
        event = Event.objects.create(
            title='Event to Review',
            description='Test',
            organizer=self.user,
            location='Test Location',
            start_time=self.start_time,
            end_time=self.end_time,
            is_public=True
        )
        
        # First RSVP as 'going'
        RSVP.objects.create(event=event, user=self.other_user, status='going')
        
        self.client.force_authenticate(user=self.other_user)
        
        data = {
            'rating': 5,
            'comment': 'Great event!'
        }
        response = self.client.post(f'/api/events/{event.id}/review/', data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['rating'], 5)


class PermissionTest(APITestCase):
    """Test custom permissions."""

    def setUp(self):
        self.organizer = User.objects.create_user(username='organizer', password='test123')
        self.invited_user = User.objects.create_user(username='invited', password='test123')
        self.uninvited_user = User.objects.create_user(username='uninvited', password='test123')
        
        self.private_event = Event.objects.create(
            title='Private Event',
            description='Test',
            organizer=self.organizer,
            location='Test Location',
            start_time=timezone.now() + timedelta(days=1),
            end_time=timezone.now() + timedelta(days=1, hours=2),
            is_public=False
        )
        
        # Simulate invitation by creating an RSVP
        RSVP.objects.create(
            event=self.private_event,
            user=self.invited_user,
            status='going'
        )

    def test_organizer_can_view_private_event(self):
        """Test that organizer can view their private event."""
        self.client.force_authenticate(user=self.organizer)
        response = self.client.get(f'/api/events/{self.private_event.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invited_user_can_view_private_event(self):
        """Test that invited users can view private event."""
        self.client.force_authenticate(user=self.invited_user)
        response = self.client.get(f'/api/events/{self.private_event.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_uninvited_user_cannot_view_private_event(self):
        """Test that uninvited users cannot view private event."""
        self.client.force_authenticate(user=self.uninvited_user)
        response = self.client.get(f'/api/events/{self.private_event.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
