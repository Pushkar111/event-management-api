<div align="center">

# 🎉 Event Management System API

[![Django CI](https://github.com/pushkarmodi/event-management-api/actions/workflows/django-ci.yml/badge.svg)](https://github.com/pushkarmodi/event-management-api/actions/workflows/django-ci.yml)
[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![Django Version](https://img.shields.io/badge/django-4.2.7-green.svg)](https://www.djangoproject.com/)
[![DRF Version](https://img.shields.io/badge/DRF-3.14%2B-red.svg)](https://www.django-rest-framework.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**A comprehensive REST API for managing events, RSVPs, and reviews built with Django and Django REST Framework.**

[Features](#-features) • [Quick Start](#-quick-start) • [API Docs](#-api-documentation) • [Testing](#-running-tests) • [Contributing](CONTRIBUTING.md)

</div>

---

## 📋 Features

- **Event Management**: Create, update, delete, and list events with public/private visibility
- **RSVP System**: Users can RSVP to events with status tracking (Going, Maybe, Not Going)
- **Review System**: Attendees can rate and review events they attended
- **User Profiles**: Extended user profiles with additional information
- **JWT Authentication**: Secure API access using JSON Web Tokens
- **Permission System**: Custom permissions for organizers and private events
- **Async Notifications**: Email notifications via Celery for event updates (Bonus)
- **Query Optimization**: Efficient database queries using select_related/prefetch_related
- **Caching**: Redis-based caching for improved performance
- **Comprehensive Tests**: Unit tests for models, serializers, and API endpoints

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Redis (for caching and Celery)
- PostgreSQL (optional, SQLite works for development)

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd "chintech network - python"
```

2. **Create virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables** (optional)
Create a `.env` file:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (optional)
DATABASE_URL=postgresql://user:password@localhost/dbname

# Redis
REDIS_URL=redis://127.0.0.1:6379/1
CELERY_BROKER_URL=redis://localhost:6379/0

# Email (for Celery notifications)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@eventmanagement.com
```

5. **Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Create superuser**
```bash
python manage.py createsuperuser
```

7. **Run development server**
```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/api/`

### Running Celery (for email notifications)

In separate terminals:

**Celery Worker:**
```bash
celery -A event_management worker -l info
```

**Celery Beat (for scheduled tasks):**
```bash
celery -A event_management beat -l info
```

## 📚 API Documentation

### Authentication

Obtain JWT token:
```bash
POST /api/token/
{
    "username": "your_username",
    "password": "your_password"
}
```

Refresh token:
```bash
POST /api/token/refresh/
{
    "refresh": "your_refresh_token"
}
```

Use the token in requests:
```bash
Authorization: Bearer <your_access_token>
```

### Event Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/events/` | List all public events (paginated) | No |
| POST | `/api/events/` | Create a new event | Yes |
| GET | `/api/events/{id}/` | Get event details | Yes (for private) |
| PUT/PATCH | `/api/events/{id}/` | Update event (organizer only) | Yes |
| DELETE | `/api/events/{id}/` | Delete event (organizer only) | Yes |
| POST | `/api/events/{id}/rsvp/` | RSVP to event | Yes |
| GET | `/api/events/{id}/rsvps/` | List event RSVPs | Yes |
| POST | `/api/events/{id}/review/` | Add event review | Yes |
| GET | `/api/events/{id}/reviews/` | List event reviews | Yes |

### RSVP Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/rsvps/` | List user's RSVPs | Yes |
| GET | `/api/rsvps/{id}/` | Get RSVP details | Yes |
| PUT/PATCH | `/api/rsvps/{id}/` | Update RSVP status | Yes (owner only) |
| DELETE | `/api/rsvps/{id}/` | Delete RSVP | Yes (owner only) |

### Review Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/reviews/` | List reviews | Yes |
| GET | `/api/reviews/{id}/` | Get review details | Yes |
| PUT/PATCH | `/api/reviews/{id}/` | Update review | Yes (owner only) |
| DELETE | `/api/reviews/{id}/` | Delete review | Yes (owner only) |

### Profile Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/profile/me/` | Get current user's profile | Yes |
| PUT/PATCH | `/api/profile/me/` | Update current user's profile | Yes |

### Example Requests

**Create Event:**
```bash
curl -X POST http://127.0.0.1:8000/api/events/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Django Meetup",
    "description": "Monthly Django developers meetup",
    "location": "Tech Hub, Downtown",
    "start_time": "2025-11-15T18:00:00Z",
    "end_time": "2025-11-15T21:00:00Z",
    "is_public": true
  }'
```

**RSVP to Event:**
```bash
curl -X POST http://127.0.0.1:8000/api/events/1/rsvp/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"status": "going"}'
```

**Add Review:**
```bash
curl -X POST http://127.0.0.1:8000/api/events/1/review/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "rating": 5,
    "comment": "Great event! Well organized."
  }'
```

**Search Events:**
```bash
curl "http://127.0.0.1:8000/api/events/?search=django&location=downtown"
```

## 🧪 Running Tests

**Run all tests:**
```bash
pytest
```

**Run with coverage:**
```bash
pytest --cov=events --cov-report=html
```

**Run Django tests:**
```bash
python manage.py test
```

**Run specific test file:**
```bash
pytest events/tests.py -v
```

## 🏗️ Project Structure

```
chintech network - python/
├── event_management/          # Django project settings
│   ├── __init__.py
│   ├── settings.py           # Project settings (DRF, JWT, Celery, Redis)
│   ├── urls.py              # Main URL configuration
│   ├── celery.py            # Celery configuration
│   ├── wsgi.py
│   └── asgi.py
├── events/                   # Main app
│   ├── models.py            # UserProfile, Event, RSVP, Review models
│   ├── serializers.py       # DRF serializers with validation
│   ├── views.py             # ViewSets with optimized queries
│   ├── permissions.py       # Custom permission classes
│   ├── urls.py              # App URL routing
│   ├── admin.py             # Django admin configuration
│   ├── tasks.py             # Celery tasks for email notifications
│   ├── signals.py           # Django signals for async task triggering
│   ├── tests.py             # Comprehensive unit tests
│   └── apps.py
├── manage.py
├── requirements.txt
├── README.md
├── PYTHONIIP01010.md        # Assignment specification
└── .github/
    └── copilot-instructions.md
```

## 🎯 Key Implementation Details

### Query Optimization

All list views use `select_related()` and `prefetch_related()` to minimize database queries:

```python
# In EventViewSet
queryset = Event.objects.select_related('organizer').annotate(
    attendee_count=Count('rsvps', filter=Q(rsvps__status='going'))
)
```

### Custom Permissions

- `IsOrganizerOrReadOnly`: Only event organizers can edit/delete their events
- `IsInvitedToPrivateEvent`: Private events visible only to organizer and invited users
- `IsOwnerOrReadOnly`: Users can only modify their own RSVPs/reviews
- `CanRSVPToEvent`: Controls who can RSVP to private events

### Caching

Event listings are cached for 5 minutes using Redis:

```python
@method_decorator(cache_page(60 * 5))
def list(self, request, *args, **kwargs):
    return super().list(request, *args, **kwargs)
```

### Background Tasks

Email notifications are sent asynchronously using Celery:
- Event creation notification to organizer
- Event update notifications to attendees
- RSVP notification to organizer
- Review notification to organizer

## 📊 Database Schema

```
User (Django built-in)
  └─ UserProfile (1:1)

Event
  ├─ organizer → User (FK)
  ├─ RSVPs (1:N)
  │   └─ user → User (FK)
  └─ Reviews (1:N)
      └─ user → User (FK)
```

## 🔒 Security Features

- JWT-based authentication
- CSRF protection enabled
- XSS prevention
- SQL injection protection via ORM
- Permission-based access control
- Private event access restrictions

## 🚢 Deployment Considerations

For production deployment:

1. Set `DEBUG=False` in settings
2. Configure proper `SECRET_KEY`
3. Set up PostgreSQL database
4. Configure email backend (SMTP)
5. Set up Redis for caching and Celery
6. Use `gunicorn` or `uvicorn` as WSGI server
7. Configure static files with WhiteNoise or CDN
8. Set up proper logging
9. Enable HTTPS
10. Configure CORS if needed

## 📝 Code Quality

The codebase follows:
- PEP 8 style guide
- Django best practices
- DRF conventions
- Comprehensive docstrings
- Type hints where applicable
- Proper error handling
- Extensive unit tests

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

**Quick Start:**
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`pytest`)
5. Commit your changes (`git commit -m 'feat: add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

Please read our [Code of Conduct](CODE_OF_CONDUCT.md) before contributing.

## 📄 Assignment Completion

This implementation fulfills all requirements from `PYTHONIIP01010.md`:

✅ Models: UserProfile, Event, RSVP, Review  
✅ API Endpoints: All required endpoints implemented  
✅ JWT Authentication: Configured and working  
✅ Custom Permissions: Organizer-only edit/delete, private event access  
✅ Pagination & Filtering: Implemented with django-filter  
✅ Query Optimization: select_related/prefetch_related used throughout  
✅ Unit Tests: Comprehensive test coverage  
✅ Bonus: Celery tasks for email notifications  

## �️ Roadmap

- [ ] Tag system for events
- [ ] Event categories
- [ ] Advanced search with filters
- [ ] Event recommendations
- [ ] Social media integration
- [ ] File upload for event images
- [ ] Calendar integration (iCal)
- [ ] GraphQL API

See the [CHANGELOG](CHANGELOG.md) for version history.

## 📞 Support & Community

- **Issues**: [GitHub Issues](https://github.com/pushkarmodi/event-management-api/issues)
- **Discussions**: [GitHub Discussions](https://github.com/pushkarmodi/event-management-api/discussions)
- **Email**: pushkarmodi111@gmail.com

For security vulnerabilities, please see [SECURITY.md](SECURITY.md).

## 📚 Documentation

- **API Usage**: See [API_USAGE.md](API_USAGE.md)
- **Development Guide**: See [DEVELOPMENT.md](DEVELOPMENT.md)
- **Getting Started**: See [GET_STARTED.md](GET_STARTED.md)
- **Quick Reference**: See [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
- **Features**: See [FEATURES.md](FEATURES.md)

## 🙏 Acknowledgments

- Django and Django REST Framework communities
- Assignment specification from ChinTech Network
- Royal Technosoft P Limited for the internship opportunity

## 📊 Project Stats

![GitHub repo size](https://img.shields.io/github/repo-size/pushkarmodi/event-management-api)
![GitHub last commit](https://img.shields.io/github/last-commit/pushkarmodi/event-management-api)
![GitHub issues](https://img.shields.io/github/issues/pushkarmodi/event-management-api)
![GitHub pull requests](https://img.shields.io/github/issues-pr/pushkarmodi/event-management-api)

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Made with ❤️ by [Pushkar Modi](https://github.com/pushkarmodi)**

⭐ Star this repo if you find it helpful!

</div>
