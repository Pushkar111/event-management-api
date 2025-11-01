# Event Management API - Quick Reference

## 🚀 Setup (First Time)

```bash
# 1. Setup environment
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # Linux/Mac

# 2. Install & migrate
pip install -r requirements.txt
python manage.py migrate

# 3. Create admin
python manage.py createsuperuser

# 4. Run server
python manage.py runserver
```

## 🔑 Authentication

```bash
# Get JWT token
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"your_user","password":"your_pass"}'

# Use token in requests
Authorization: Bearer YOUR_ACCESS_TOKEN
```

## 📍 Key Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/token/` | Get JWT token |
| GET | `/api/events/` | List events |
| POST | `/api/events/` | Create event |
| GET | `/api/events/{id}/` | Event details |
| PUT | `/api/events/{id}/` | Update event |
| DELETE | `/api/events/{id}/` | Delete event |
| POST | `/api/events/{id}/rsvp/` | RSVP to event |
| POST | `/api/events/{id}/review/` | Add review |

## 📝 Common Commands

```bash
# Development
python manage.py runserver              # Start server
python manage.py shell                  # Django shell
python manage.py createsuperuser       # Create admin

# Database
python manage.py makemigrations        # Create migrations
python manage.py migrate               # Apply migrations
python manage.py showmigrations        # Show migration status

# Testing
pytest                                 # Run all tests
pytest --cov=events                   # With coverage
python manage.py test                 # Django test runner

# Celery (in separate terminals)
redis-server                          # Start Redis
celery -A event_management worker -l info    # Celery worker
celery -A event_management beat -l info      # Celery beat

# Code Quality
black .                               # Format code
isort .                               # Sort imports
flake8                                # Lint code
```

## 🐳 Docker Quick Start

```bash
# Start everything
docker-compose up

# Stop everything
docker-compose down

# View logs
docker-compose logs -f web
```

## 📊 Example API Calls

### Create Event
```bash
curl -X POST http://127.0.0.1:8000/api/events/ \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My Event",
    "description": "Event description",
    "location": "Location",
    "start_time": "2025-12-01T10:00:00Z",
    "end_time": "2025-12-01T12:00:00Z",
    "is_public": true
  }'
```

### RSVP to Event
```bash
curl -X POST http://127.0.0.1:8000/api/events/1/rsvp/ \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status": "going"}'
```

### Add Review
```bash
curl -X POST http://127.0.0.1:8000/api/events/1/review/ \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"rating": 5, "comment": "Great event!"}'
```

### Search Events
```bash
curl "http://127.0.0.1:8000/api/events/?search=django&is_public=true"
```

## 🗂️ Project Structure

```
events/
├── models.py        # UserProfile, Event, RSVP, Review
├── serializers.py   # DRF serializers
├── views.py         # ViewSets
├── permissions.py   # Custom permissions
├── tasks.py         # Celery tasks
├── signals.py       # Django signals
├── admin.py         # Admin config
├── urls.py          # URL routing
└── tests.py         # Unit tests
```

## 🔒 Permissions

- **IsOrganizerOrReadOnly** - Only organizers can edit/delete events
- **IsInvitedToPrivateEvent** - Access to private events
- **IsOwnerOrReadOnly** - Own RSVPs/reviews only

## 📦 Key Models

```python
# Event
Event(title, description, organizer, location, 
      start_time, end_time, is_public)

# RSVP
RSVP(event, user, status=['going','maybe','not_going'])

# Review
Review(event, user, rating=1-5, comment)

# UserProfile
UserProfile(user, full_name, bio, location, profile_picture)
```

## 🐛 Troubleshooting

```bash
# Module not found errors
pip install -r requirements.txt

# Migration issues
python manage.py migrate --fake-initial

# Redis connection refused
redis-server  # Start Redis

# Permission denied
# Check authentication token and user permissions
```

## 📚 Documentation

- `README.md` - Full documentation
- `API_USAGE.md` - API examples
- `DEVELOPMENT.md` - Developer guide
- `PROJECT_SUMMARY.md` - Project overview

## 🎯 Admin Panel

Access at: http://127.0.0.1:8000/admin/
- Manage users, events, RSVPs, reviews
- View statistics and relationships
- Test data creation

## 🧪 Testing Tips

```python
# Run specific test
pytest events/tests.py::EventAPITest::test_create_event_authenticated -v

# Debug with print
pytest -s  # Show print statements

# Generate coverage report
pytest --cov=events --cov-report=html
open htmlcov/index.html
```

## 🚀 Production Checklist

- [ ] Set DEBUG=False
- [ ] Configure SECRET_KEY
- [ ] Set up PostgreSQL
- [ ] Configure email backend
- [ ] Set up Redis
- [ ] Configure static files
- [ ] Enable HTTPS
- [ ] Set up monitoring

---

**Need more info?** Check the full documentation in `README.md`
