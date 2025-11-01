"""
Management command to create sample data for testing.
Usage: python manage.py create_sample_data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from events.models import UserProfile, Event, RSVP, Review


class Command(BaseCommand):
    help = 'Creates sample data for testing the Event Management System'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Creating sample data...'))

        # Create users
        users = []
        for i in range(1, 6):
            user, created = User.objects.get_or_create(
                username=f'user{i}',
                defaults={
                    'email': f'user{i}@yopmail.com',
                    'first_name': f'User{i}',
                    'last_name': 'Test'
                }
            )
            if created:
                user.set_password('password123')
                user.save()
                self.stdout.write(f'Created user: {user.username}')
            
            # Create user profile
            profile, created = UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    'full_name': f'User {i} Full Name',
                    'bio': f'Bio for user {i}',
                    'location': f'City {i}'
                }
            )
            users.append(user)

        # Create events
        events = []
        now = timezone.now()
        
        event_data = [
            {
                'title': 'Django Conference 2025',
                'description': 'Annual Django developers conference with talks and workshops',
                'location': 'Convention Center, San Francisco',
                'days_ahead': 30,
                'is_public': True
            },
            {
                'title': 'Python Meetup',
                'description': 'Monthly Python developers meetup',
                'location': 'Tech Hub Downtown',
                'days_ahead': 15,
                'is_public': True
            },
            {
                'title': 'DRF Workshop',
                'description': 'Hands-on workshop on Django REST Framework',
                'location': 'Online',
                'days_ahead': 7,
                'is_public': True
            },
            {
                'title': 'Private Team Event',
                'description': 'Company internal event',
                'location': 'Office',
                'days_ahead': 3,
                'is_public': False
            },
            {
                'title': 'Web Development Bootcamp',
                'description': 'Intensive web development training',
                'location': 'Training Center',
                'days_ahead': 60,
                'is_public': True
            }
        ]

        for i, data in enumerate(event_data):
            start_time = now + timedelta(days=data['days_ahead'])
            end_time = start_time + timedelta(hours=3)
            
            event, created = Event.objects.get_or_create(
                title=data['title'],
                defaults={
                    'description': data['description'],
                    'organizer': users[i % len(users)],
                    'location': data['location'],
                    'start_time': start_time,
                    'end_time': end_time,
                    'is_public': data['is_public']
                }
            )
            if created:
                self.stdout.write(f'Created event: {event.title}')
            events.append(event)

        # Create RSVPs
        rsvp_count = 0
        for event in events[:3]:  # First 3 events
            for user in users[:3]:  # First 3 users
                if event.organizer != user:
                    rsvp, created = RSVP.objects.get_or_create(
                        event=event,
                        user=user,
                        defaults={'status': 'going'}
                    )
                    if created:
                        rsvp_count += 1

        self.stdout.write(f'Created {rsvp_count} RSVPs')

        # Create Reviews
        review_count = 0
        for event in events[:2]:  # First 2 events
            for user in users[:2]:  # First 2 users
                if event.organizer != user:
                    # Make sure user has RSVP'd as 'going'
                    RSVP.objects.get_or_create(
                        event=event,
                        user=user,
                        defaults={'status': 'going'}
                    )
                    
                    review, created = Review.objects.get_or_create(
                        event=event,
                        user=user,
                        defaults={
                            'rating': 5,
                            'comment': f'Great event! Enjoyed it very much.'
                        }
                    )
                    if created:
                        review_count += 1

        self.stdout.write(f'Created {review_count} reviews')

        self.stdout.write(self.style.SUCCESS('\nSample data creation complete!'))
        self.stdout.write(self.style.SUCCESS('\nYou can now login with:'))
        self.stdout.write('  Username: user1 to user5')
        self.stdout.write('  Password: password123')
        self.stdout.write('\nGet JWT token with:')
        self.stdout.write('  curl -X POST http://127.0.0.1:8000/api/token/ \\')
        self.stdout.write('    -H "Content-Type: application/json" \\')
        self.stdout.write('    -d \'{"username":"user1","password":"password123"}\'')
