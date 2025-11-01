"""
Django signals for Event Management System.

Automatically trigger Celery tasks for email notifications
when models are created or updated.

Following best practices:
- Use post_save signals for async task triggering
- Check for created flag to distinguish creates from updates
- Avoid infinite loops with proper signal handling
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Event, RSVP, Review
from .tasks import (
    send_event_creation_notification,
    send_event_update_notification,
    send_rsvp_notification_to_organizer,
    send_review_notification
)
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Event)
def event_post_save(sender, instance, created, **kwargs):
    """
    Trigger email notifications when an event is created or updated.
    """
    if created:
        # New event created - notify organizer
        try:
            send_event_creation_notification.delay(
                event_id=instance.id,
                organizer_id=instance.organizer.id
            )
            logger.info(f"Queued creation notification for event {instance.id}")
        except Exception as e:
            logger.error(f"Error queuing event creation notification: {str(e)}")
    else:
        # Event updated - notify attendees
        # In production, you'd track which fields changed
        try:
            # For simplicity, we'll just say "Event details updated"
            send_event_update_notification.delay(
                event_id=instance.id,
                updated_fields=['Event details']
            )
            logger.info(f"Queued update notification for event {instance.id}")
        except Exception as e:
            logger.error(f"Error queuing event update notification: {str(e)}")


@receiver(post_save, sender=RSVP)
def rsvp_post_save(sender, instance, created, **kwargs):
    """
    Trigger email notification to organizer when someone RSVPs.
    """
    try:
        send_rsvp_notification_to_organizer.delay(rsvp_id=instance.id)
        logger.info(f"Queued RSVP notification for RSVP {instance.id}")
    except Exception as e:
        logger.error(f"Error queuing RSVP notification: {str(e)}")


@receiver(post_save, sender=Review)
def review_post_save(sender, instance, created, **kwargs):
    """
    Trigger email notification to organizer when someone reviews their event.
    """
    if created:
        try:
            send_review_notification.delay(review_id=instance.id)
            logger.info(f"Queued review notification for review {instance.id}")
        except Exception as e:
            logger.error(f"Error queuing review notification: {str(e)}")
