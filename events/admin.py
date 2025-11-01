"""
Django admin configuration for Event Management System.

Following best practices:
- Customized admin displays with list_display
- Search and filter capabilities
- Readonly fields for timestamps
- Inline editing for related models
"""
from django.contrib import admin
from .models import UserProfile, Event, RSVP, Review


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin interface for UserProfile."""
    
    list_display = ['user', 'full_name', 'location', 'created_at']
    search_fields = ['user__username', 'user__email', 'full_name']
    list_filter = ['created_at']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'full_name', 'bio')
        }),
        ('Additional Details', {
            'fields': ('location', 'profile_picture')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


class RSVPInline(admin.TabularInline):
    """Inline admin for RSVPs within Event admin."""
    
    model = RSVP
    extra = 0
    readonly_fields = ['created_at', 'updated_at']
    fields = ['user', 'status', 'created_at']


class ReviewInline(admin.TabularInline):
    """Inline admin for Reviews within Event admin."""
    
    model = Review
    extra = 0
    readonly_fields = ['created_at', 'updated_at']
    fields = ['user', 'rating', 'comment', 'created_at']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """Admin interface for Event with inline RSVPs and Reviews."""
    
    list_display = [
        'title', 'organizer', 'location', 'start_time',
        'is_public', 'attendee_count', 'created_at'
    ]
    search_fields = ['title', 'description', 'location', 'organizer__username']
    list_filter = ['is_public', 'start_time', 'created_at']
    readonly_fields = ['created_at', 'updated_at', 'attendee_count']
    date_hierarchy = 'start_time'
    inlines = [RSVPInline, ReviewInline]
    
    fieldsets = (
        ('Event Information', {
            'fields': ('title', 'description', 'organizer')
        }),
        ('Location & Time', {
            'fields': ('location', 'start_time', 'end_time')
        }),
        ('Settings', {
            'fields': ('is_public',)
        }),
        ('Statistics', {
            'fields': ('attendee_count',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def attendee_count(self, obj):
        """Display count of confirmed attendees."""
        return obj.attendee_count
    attendee_count.short_description = 'Attendees'


@admin.register(RSVP)
class RSVPAdmin(admin.ModelAdmin):
    """Admin interface for RSVP."""
    
    list_display = ['user', 'event', 'status', 'created_at']
    search_fields = ['user__username', 'event__title']
    list_filter = ['status', 'created_at']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('RSVP Details', {
            'fields': ('event', 'user', 'status')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Admin interface for Review."""
    
    list_display = ['user', 'event', 'rating', 'created_at']
    search_fields = ['user__username', 'event__title', 'comment']
    list_filter = ['rating', 'created_at']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Review Details', {
            'fields': ('event', 'user', 'rating', 'comment')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
