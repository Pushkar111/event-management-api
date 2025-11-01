# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Event categories and tags
- Event search filters (by date range, location)
- User follow/unfollow for organizers
- Event recommendations based on user interests
- Export events to calendar formats (iCal, Google Calendar)

## [1.0.0] - 2025-11-01

### Added
- **Core Features**
  - User authentication with JWT tokens
  - User profile management with custom fields
  - Event CRUD operations with permissions
  - RSVP system (Going, Maybe, Not Going)
  - Event reviews and ratings (1-5 stars)
  - Public and private events
  
- **API Endpoints**
  - `/api/token/` - JWT token authentication
  - `/api/token/refresh/` - Refresh JWT tokens
  - `/api/events/` - Event management
  - `/api/events/{id}/rsvp/` - RSVP to events
  - `/api/events/{id}/review/` - Review events
  - `/api/profiles/me/` - User profile management
  - `/api/rsvps/` - RSVP management
  - `/api/reviews/` - Review management

- **Authentication & Authorization**
  - JWT authentication for API access
  - Session authentication for browsable API
  - Custom permissions (IsOrganizerOrReadOnly, IsOwnerOrReadOnly)
  - Private event access control

- **Performance Optimization**
  - Query optimization with select_related/prefetch_related
  - Redis caching for frequently accessed data
  - Database indexing on key fields
  - Pagination for list endpoints

- **Background Tasks**
  - Celery integration for async tasks
  - Email notifications for:
    - Event creation confirmation
    - RSVP confirmations
    - New review notifications to organizers
  - Redis as Celery broker

- **Testing**
  - Comprehensive test suite with pytest
  - Unit tests for models, serializers, views
  - API endpoint tests
  - Permission tests
  - 80%+ code coverage

- **Documentation**
  - Complete API documentation
  - Setup guides (Quick Start, Development)
  - API usage examples (curl, Python, JavaScript)
  - Docker deployment guide
  - Troubleshooting guide

- **Developer Tools**
  - Sample data creation command
  - Docker and docker-compose support
  - Development and production settings
  - Comprehensive .gitignore
  - Pre-configured VS Code settings

### Security
- CSRF protection enabled
- SQL injection protection (Django ORM)
- XSS protection
- Secure password hashing (PBKDF2)
- Environment variable configuration for secrets
- JWT token expiration and refresh

### Changed
- N/A (initial release)

### Deprecated
- N/A (initial release)

### Removed
- N/A (initial release)

### Fixed
- N/A (initial release)

## Version History

### [1.0.0] - 2025-11-01
- Initial release with core functionality

---

## Release Notes

### v1.0.0 - Initial Release

This is the first stable release of the Event Management API. It includes all core features required for managing events, RSVPs, and reviews with full authentication and authorization.

**Key Features:**
- Complete REST API with Django REST Framework
- JWT authentication
- Event management (CRUD)
- RSVP system
- Review and rating system
- Async email notifications with Celery
- Query optimization and caching
- Comprehensive test coverage
- Docker support

**Requirements:**
- Python 3.11+
- Django 4.2+
- PostgreSQL 13+ (or SQLite for development)
- Redis 6+

**Breaking Changes:**
- None (initial release)

**Migration Guide:**
- None (initial release)

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute to this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
