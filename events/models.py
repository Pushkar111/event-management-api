"""
Models for Event Management System.

Following Django best practices:
- Business logic in models
- Proper use of ForeignKey and related_name
- Timestamps with auto_now_add and auto_now
- Choices for constrained fields
- Clear __str__ methods for admin interface
"""
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class UserProfile(models.Model):
    """
    Extended user profile with additional information.
    OneToOne relationship with Django's built-in User model.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    full_name = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=255, blank=True)
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}'s Profile"

    @property
    def display_name(self):
        """Return full_name if available, otherwise username."""
        return self.full_name or self.user.username


class Event(models.Model):
    """
    Event model representing an event in the system.
    Contains all event details including organizer, location, and timing.
    """
    title = models.CharField(max_length=255, db_index=True)
    description = models.TextField()
    organizer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='organized_events'
    )
    location = models.CharField(max_length=255, db_index=True)
    start_time = models.DateTimeField(db_index=True)
    end_time = models.DateTimeField()
    is_public = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
        ordering = ['-start_time']
        indexes = [
            models.Index(fields=['organizer', 'is_public']),
            models.Index(fields=['start_time', 'is_public']),
        ]

    def __str__(self):
        return f"{self.title} by {self.organizer.username}"

    def clean(self):
        """Validate that end_time is after start_time."""
        from django.core.exceptions import ValidationError
        if self.end_time and self.start_time and self.end_time <= self.start_time:
            raise ValidationError({
                'end_time': 'End time must be after start time.'
            })

    def save(self, *args, **kwargs):
        """Override save to call full_clean for validation."""
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def is_upcoming(self):
        """Check if event is in the future."""
        return self.start_time > timezone.now()

    @property
    def is_ongoing(self):
        """Check if event is currently happening."""
        now = timezone.now()
        return self.start_time <= now <= self.end_time

    @property
    def attendee_count(self):
        """Get count of confirmed attendees (Going status)."""
        return self.rsvps.filter(status='going').count()


class RSVP(models.Model):
    """
    RSVP model for tracking user responses to events.
    Ensures one RSVP per user per event with unique_together constraint.
    """
    STATUS_CHOICES = [
        ('going', 'Going'),
        ('maybe', 'Maybe'),
        ('not_going', 'Not Going'),
    ]

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='rsvps'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='rsvps'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='going'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'RSVP'
        verbose_name_plural = 'RSVPs'
        ordering = ['-created_at']
        unique_together = ['event', 'user']
        indexes = [
            models.Index(fields=['event', 'status']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.event.title} ({self.get_status_display()})"


class Review(models.Model):
    """
    Review model for event feedback.
    Allows users to rate and comment on events they attended.
    """
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        ordering = ['-created_at']
        unique_together = ['event', 'user']
        indexes = [
            models.Index(fields=['event', 'rating']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.event.title} ({self.rating}/5)"

    def clean(self):
        """Validate that rating is between 1 and 5."""
        from django.core.exceptions import ValidationError
        if self.rating and (self.rating < 1 or self.rating > 5):
            raise ValidationError({
                'rating': 'Rating must be between 1 and 5.'
            })

    def save(self, *args, **kwargs):
        """Override save to call full_clean for validation."""
        self.full_clean()
        super().save(*args, **kwargs)
