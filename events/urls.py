"""
URL routing for events app.

Using DRF DefaultRouter for automatic URL generation.
Includes nested routes for RSVPs and reviews within events.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, RSVPViewSet, ReviewViewSet, UserProfileViewSet

# Create router and register viewsets
router = DefaultRouter()
router.register(r'events', EventViewSet, basename='event')
router.register(r'rsvps', RSVPViewSet, basename='rsvp')
router.register(r'reviews', ReviewViewSet, basename='review')
router.register(r'profile', UserProfileViewSet, basename='profile')

urlpatterns = [
    path('', include(router.urls)),
]
