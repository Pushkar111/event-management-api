"""
Custom DRF permissions for Event Management System.

Following Django REST Framework permission patterns:
- has_permission for view-level checks
- has_object_permission for object-level checks
- Clear error messages for denied access
"""
from rest_framework import permissions


class IsOrganizerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow organizers of an event to edit/delete it.
    Read-only access is allowed for all authenticated users.
    """
    
    message = "You must be the event organizer to perform this action."

    def has_object_permission(self, request, view, obj):
        """
        Read permissions are allowed for any safe method (GET, HEAD, OPTIONS).
        Write permissions are only allowed to the organizer.
        """
        # Allow read operations for authenticated users
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions only for the organizer
        return obj.organizer == request.user


class IsInvitedToPrivateEvent(permissions.BasePermission):
    """
    Custom permission to restrict access to private events.
    Only the organizer and invited users can view private events.
    
    In a production app, this would check an Invitation model.
    For this assignment, we check if user has an RSVP.
    """
    
    message = "You don't have access to this private event."

    def has_object_permission(self, request, view, obj):
        """
        For private events, only organizer and users with RSVPs can access.
        Public events are accessible to all authenticated users.
        """
        # Public events are accessible to all
        if obj.is_public:
            return True

        # Private events: check if user is organizer
        if obj.organizer == request.user:
            return True

        # Check if user has an RSVP (simulating invitation)
        from events.models import RSVP
        has_rsvp = RSVP.objects.filter(
            event=obj,
            user=request.user
        ).exists()

        return has_rsvp


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission for RSVP and Review models.
    Only the owner can modify their RSVP/Review.
    """
    
    message = "You can only modify your own RSVPs and reviews."

    def has_object_permission(self, request, view, obj):
        """
        Read permissions for authenticated users.
        Write permissions only for the owner.
        """
        # Read operations allowed for all authenticated users
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write operations only for the owner
        return obj.user == request.user


class CanRSVPToEvent(permissions.BasePermission):
    """
    Custom permission to check if user can RSVP to an event.
    Users can RSVP to public events or private events they're invited to.
    """
    
    message = "You cannot RSVP to this private event."

    def has_permission(self, request, view):
        """Allow authenticated users to attempt RSVP."""
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Check if user can RSVP to the event.
        For private events, check if user is organizer or already has RSVP.
        """
        # Public events: anyone can RSVP
        if obj.is_public:
            return True

        # Private events: organizer can always RSVP
        if obj.organizer == request.user:
            return True

        # Check if user already has an RSVP (invitation simulation)
        from events.models import RSVP
        has_rsvp = RSVP.objects.filter(
            event=obj,
            user=request.user
        ).exists()

        return has_rsvp
