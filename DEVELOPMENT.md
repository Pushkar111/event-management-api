# Development Guide

## Project Overview

This Event Management System is built following Django and DRF best practices as outlined in the `.cursor/rules/` and `.github/copilot-instructions.md`.

## Architecture

### MVT Pattern (Model-View-Template)
- **Models** (`events/models.py`): Business logic and data structure
- **Views** (`events/views.py`): Request handling via DRF ViewSets
- **Serializers** (`events/serializers.py`): Data validation and transformation

### Key Components

```
┌─────────────────────────────────────────────────┐
│                    Client                        │
│            (Browser, Mobile App, etc)           │
└──────────────────┬──────────────────────────────┘
                   │ HTTP/JSON
                   ▼
┌─────────────────────────────────────────────────┐
│              Django REST Framework               │
│  ┌─────────────────────────────────────────┐   │
│  │  Authentication (JWT)                   │   │
│  │  ↓                                       │   │
│  │  Permissions (Custom)                   │   │
│  │  ↓                                       │   │
│  │  ViewSets (with query optimization)     │   │
│  │  ↓                                       │   │
│  │  Serializers (validation)               │   │
│  │  ↓                                       │   │
│  │  Models (business logic)                │   │
│  └─────────────────────────────────────────┘   │
└──────────────────┬──────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────┐
│            Database (PostgreSQL/SQLite)         │
└─────────────────────────────────────────────────┘

         Async Tasks (via Django Signals)
                   │
                   ▼
┌─────────────────────────────────────────────────┐
│               Celery Worker                      │
│          (Email Notifications)                   │
└──────────────────┬──────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────┐
│              Redis (Broker)                      │
└─────────────────────────────────────────────────┘
```

## Code Organization

### Models Design

All models follow these principles:
- Business logic in models (e.g., `attendee_count`, `is_upcoming`)
- Proper indexes on frequently queried fields
- Validation in `clean()` method
- Proper `__str__()` for admin interface
- Related names for reverse relationships

Example from `Event` model:
```python
class Event(models.Model):
    # Fields with indexes
    title = models.CharField(max_length=255, db_index=True)
    
    # Related fields with proper related_name
    organizer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='organized_events'
    )
    
    # Business logic as properties
    @property
    def attendee_count(self):
        return self.rsvps.filter(status='going').count()
```

### ViewSets Optimization

All viewsets implement query optimization:

```python
def get_queryset(self):
    # Use select_related for FK/OneToOne
    # Use prefetch_related for Many relations
    return Event.objects.select_related('organizer').annotate(
        attendee_count=Count('rsvps', filter=Q(rsvps__status='going'))
    )
```

### Permissions System

Custom permissions are implemented for:
1. **IsOrganizerOrReadOnly**: Only organizers can edit/delete events
2. **IsInvitedToPrivateEvent**: Access control for private events
3. **IsOwnerOrReadOnly**: Users can only modify their own RSVPs/reviews

### Serializers

Multiple serializers for different use cases:
- `EventListSerializer`: Lightweight for listing
- `EventDetailSerializer`: Full data with nested relations
- `EventCreateUpdateSerializer`: Separate for write operations

## Development Workflow

### 1. Setting Up Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### 2. Running Development Server

```bash
# Start Django server
python manage.py runserver

# In another terminal, start Redis
redis-server

# In another terminal, start Celery worker
celery -A event_management worker -l info

# Optional: Start Celery beat for scheduled tasks
celery -A event_management beat -l info
```

### 3. Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=events --cov-report=html

# Run specific test file
pytest events/tests.py -v

# Run specific test class
pytest events/tests.py::EventAPITest -v

# Run specific test method
pytest events/tests.py::EventAPITest::test_create_event_authenticated -v
```

### 4. Code Quality Checks

```bash
# Format code with black
black .

# Sort imports
isort .

# Lint with flake8
flake8

# Type checking (if using mypy)
mypy events/
```

### 5. Making Changes

When adding a new feature:

1. **Update models** (if needed) in `events/models.py`
2. **Create/update serializers** in `events/serializers.py`
3. **Add/update viewsets** in `events/views.py`
4. **Add custom permissions** (if needed) in `events/permissions.py`
5. **Update URLs** (if needed) in `events/urls.py`
6. **Write tests** in `events/tests.py`
7. **Run migrations** if models changed
8. **Update documentation**

### 6. Database Migrations

```bash
# Create migrations
python manage.py makemigrations

# View SQL for migration
python manage.py sqlmigrate events 0001

# Apply migrations
python manage.py migrate

# Rollback migration
python manage.py migrate events 0001_initial
```

## Best Practices (from .cursorrules)

### Query Optimization

Always use:
- `select_related()` for ForeignKey and OneToOne
- `prefetch_related()` for ManyToMany and reverse ForeignKey
- `annotate()` for computed fields
- `only()` or `defer()` when you don't need all fields

Example:
```python
# Good
events = Event.objects.select_related('organizer').prefetch_related(
    'rsvps__user', 'reviews'
).filter(is_public=True)

# Bad (N+1 queries)
events = Event.objects.filter(is_public=True)
for event in events:
    print(event.organizer.username)  # Extra query per event
```

### Caching

Use Django's cache framework:
```python
from django.core.cache import cache
from django.views.decorators.cache import cache_page

# Cache view for 5 minutes
@method_decorator(cache_page(60 * 5))
def list(self, request, *args, **kwargs):
    return super().list(request, *args, **kwargs)

# Manual caching
def get_event_stats(event_id):
    cache_key = f'event_stats_{event_id}'
    stats = cache.get(cache_key)
    if stats is None:
        stats = calculate_stats(event_id)
        cache.set(cache_key, stats, 300)  # 5 minutes
    return stats
```

### Async Tasks

Use Celery for:
- Email notifications
- Long-running computations
- External API calls
- Periodic tasks

Example:
```python
# In signals.py
@receiver(post_save, sender=Event)
def event_post_save(sender, instance, created, **kwargs):
    if created:
        send_event_creation_notification.delay(
            event_id=instance.id,
            organizer_id=instance.organizer.id
        )
```

### Security

Always:
- Use JWT for authentication
- Implement proper permissions
- Validate input in serializers
- Use Django's built-in protections (CSRF, XSS, SQL injection)
- Never expose sensitive data in API responses
- Use HTTPS in production

## Common Tasks

### Adding a New Model

1. Define model in `events/models.py`
2. Create serializer in `events/serializers.py`
3. Create viewset in `events/views.py`
4. Register in admin in `events/admin.py`
5. Add URL routing in `events/urls.py`
6. Write tests in `events/tests.py`
7. Run `python manage.py makemigrations`
8. Run `python manage.py migrate`

### Adding a New API Endpoint

1. Add method to viewset with `@action` decorator:
```python
@action(detail=True, methods=['post'])
def custom_action(self, request, pk=None):
    obj = self.get_object()
    # Your logic here
    return Response({'status': 'success'})
```

2. Test the endpoint
3. Update documentation

### Debugging

```bash
# Use Django shell
python manage.py shell

# Import models and test
from events.models import Event, User
events = Event.objects.select_related('organizer').all()

# Check generated SQL
from django.db import connection
print(connection.queries)

# Use Django Debug Toolbar (add to requirements if needed)
pip install django-debug-toolbar
```

## Performance Monitoring

### Query Analysis

```python
from django.db import connection
from django.test.utils import override_settings

@override_settings(DEBUG=True)
def test_view():
    response = client.get('/api/events/')
    print(f"Number of queries: {len(connection.queries)}")
    for query in connection.queries:
        print(query['sql'])
```

### Celery Monitoring

```bash
# Monitor Celery tasks
celery -A event_management events

# Inspect active tasks
celery -A event_management inspect active

# Check task stats
celery -A event_management inspect stats
```

## Troubleshooting

### Common Issues

1. **ImportError: No module named 'rest_framework'**
   - Solution: Install dependencies: `pip install -r requirements.txt`

2. **No migrations to apply**
   - Solution: Run `python manage.py makemigrations events`

3. **Connection refused (Redis)**
   - Solution: Start Redis: `redis-server`

4. **Permission denied on endpoint**
   - Solution: Check authentication and custom permissions

5. **Celery not picking up tasks**
   - Solution: Restart Celery worker and check signals are connected

## Production Deployment

See `README.md` for production deployment checklist.

Key points:
- Set `DEBUG=False`
- Use environment variables for secrets
- Use PostgreSQL instead of SQLite
- Configure email backend
- Set up proper logging
- Use gunicorn/uvicorn
- Configure static files with WhiteNoise or CDN
- Enable HTTPS
- Set up monitoring (Sentry, etc.)

## Resources

- Django Docs: https://docs.djangoproject.com/
- DRF Docs: https://www.django-rest-framework.org/
- Celery Docs: https://docs.celeryproject.org/
- Project cursor rules: `.cursor/rules/python-django-best-practices-cursorrules-prompt-fi/`
- Assignment spec: `PYTHONIIP01010.md`
