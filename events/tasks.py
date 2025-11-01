"""
Celery tasks for Event Management System.

Implements asynchronous email notifications for:
- Event creation
- Event updates
- RSVP notifications to organizers
- Review notifications

Following best practices:
- Tasks are idempotent
- Proper error handling
- Logging for debugging
"""
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
import logging

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def send_event_creation_notification(self, event_id, organizer_id):
    """
    Send email notification when a new event is created.
    
    Args:
        event_id: ID of the created event
        organizer_id: ID of the event organizer
    """
    try:
        from events.models import Event
        
        event = Event.objects.get(id=event_id)
        organizer = User.objects.get(id=organizer_id)
        
        subject = f'Event Created: {event.title}'
        message = f"""
        Hello {organizer.username},
        
        Your event "{event.title}" has been successfully created!
        
        Event Details:
        - Title: {event.title}
        - Location: {event.location}
        - Start Time: {event.start_time}
        - End Time: {event.end_time}
        - Visibility: {'Public' if event.is_public else 'Private'}
        
        You can manage your event through the API.
        
        Best regards,
        Event Management Team
        """
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [organizer.email],
            fail_silently=False,
        )
        
        logger.info(f"Event creation notification sent for event {event_id}")
        return f"Email sent to {organizer.email}"
        
    except Exception as exc:
        logger.error(f"Error sending event creation notification: {str(exc)}")
        raise self.retry(exc=exc, countdown=60)


@shared_task(bind=True, max_retries=3)
def send_event_update_notification(self, event_id, updated_fields):
    """
    Send email notification to all attendees when an event is updated.
    
    Args:
        event_id: ID of the updated event
        updated_fields: List of field names that were updated
    """
    try:
        from events.models import Event, RSVP
        
        event = Event.objects.get(id=event_id)
        
        # Get all users who RSVP'd as 'going'
        rsvps = RSVP.objects.filter(
            event=event,
            status='going'
        ).select_related('user')
        
        attendee_emails = [rsvp.user.email for rsvp in rsvps if rsvp.user.email]
        
        if not attendee_emails:
            logger.info(f"No attendees to notify for event {event_id}")
            return "No attendees to notify"
        
        subject = f'Event Updated: {event.title}'
        message = f"""
        Hello,
        
        The event "{event.title}" you're attending has been updated.
        
        Updated fields: {', '.join(updated_fields)}
        
        Current Event Details:
        - Title: {event.title}
        - Location: {event.location}
        - Start Time: {event.start_time}
        - End Time: {event.end_time}
        
        Please check the latest details through the API.
        
        Best regards,
        Event Management Team
        """
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            attendee_emails,
            fail_silently=False,
        )
        
        logger.info(f"Event update notification sent to {len(attendee_emails)} attendees")
        return f"Email sent to {len(attendee_emails)} attendees"
        
    except Exception as exc:
        logger.error(f"Error sending event update notification: {str(exc)}")
        raise self.retry(exc=exc, countdown=60)


@shared_task(bind=True, max_retries=3)
def send_rsvp_notification_to_organizer(self, rsvp_id):
    """
    Send email notification to event organizer when someone RSVPs.
    
    Args:
        rsvp_id: ID of the RSVP
    """
    try:
        from events.models import RSVP
        
        rsvp = RSVP.objects.select_related('event', 'user').get(id=rsvp_id)
        organizer = rsvp.event.organizer
        
        if not organizer.email:
            logger.info(f"Organizer has no email for RSVP {rsvp_id}")
            return "Organizer has no email"
        
        subject = f'New RSVP for {rsvp.event.title}'
        message = f"""
        Hello {organizer.username},
        
        {rsvp.user.username} has RSVP'd to your event "{rsvp.event.title}".
        
        Status: {rsvp.get_status_display()}
        
        You can view all RSVPs for your event through the API.
        
        Best regards,
        Event Management Team
        """
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [organizer.email],
            fail_silently=False,
        )
        
        logger.info(f"RSVP notification sent to organizer for RSVP {rsvp_id}")
        return f"Email sent to {organizer.email}"
        
    except Exception as exc:
        logger.error(f"Error sending RSVP notification: {str(exc)}")
        raise self.retry(exc=exc, countdown=60)


@shared_task(bind=True, max_retries=3)
def send_review_notification(self, review_id):
    """
    Send email notification to event organizer when someone reviews their event.
    
    Args:
        review_id: ID of the review
    """
    try:
        from events.models import Review
        
        review = Review.objects.select_related('event', 'user').get(id=review_id)
        organizer = review.event.organizer
        
        if not organizer.email:
            logger.info(f"Organizer has no email for review {review_id}")
            return "Organizer has no email"
        
        subject = f'New Review for {review.event.title}'
        message = f"""
        Hello {organizer.username},
        
        {review.user.username} has reviewed your event "{review.event.title}".
        
        Rating: {review.rating}/5
        Comment: {review.comment}
        
        You can view all reviews for your event through the API.
        
        Best regards,
        Event Management Team
        """
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [organizer.email],
            fail_silently=False,
        )
        
        logger.info(f"Review notification sent to organizer for review {review_id}")
        return f"Email sent to {organizer.email}"
        
    except Exception as exc:
        logger.error(f"Error sending review notification: {str(exc)}")
        raise self.retry(exc=exc, countdown=60)


@shared_task
def cleanup_old_events():
    """
    Periodic task to archive or clean up old events.
    Can be scheduled with Celery Beat.
    """
    from events.models import Event
    from django.utils import timezone
    from datetime import timedelta
    
    # Find events that ended more than 30 days ago
    cutoff_date = timezone.now() - timedelta(days=30)
    old_events = Event.objects.filter(end_time__lt=cutoff_date)
    
    count = old_events.count()
    logger.info(f"Found {count} events older than 30 days")
    
    # In a real app, you might archive these instead of deleting
    # For now, we'll just log them
    return f"Found {count} old events"
