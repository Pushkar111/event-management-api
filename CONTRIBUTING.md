# Contributing to Event Management System

Thank you for considering contributing to this Event Management System! 🎉

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Submitting Changes](#submitting-changes)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Features](#suggesting-features)

## Code of Conduct

This project adheres to a code of conduct. By participating, you are expected to:
- Be respectful and inclusive
- Accept constructive criticism gracefully
- Focus on what is best for the community
- Show empathy towards other community members

## Getting Started

### Prerequisites
- Python 3.11+
- PostgreSQL 13+ or SQLite (for development)
- Redis 6+
- Git

### Setup Development Environment

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/Pushkar111/event-management-api.git
   cd event-management-api
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configurations
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create sample data**
   ```bash
   python manage.py create_sample_data
   ```

7. **Run tests**
   ```bash
   pytest
   ```

## Development Workflow

### Branch Naming Convention

- `feature/` - New features (e.g., `feature/add-event-tags`)
- `bugfix/` - Bug fixes (e.g., `bugfix/fix-rsvp-validation`)
- `hotfix/` - Critical fixes for production (e.g., `hotfix/security-patch`)
- `refactor/` - Code refactoring (e.g., `refactor/optimize-queries`)
- `docs/` - Documentation updates (e.g., `docs/update-api-guide`)
- `test/` - Adding or updating tests (e.g., `test/add-event-tests`)

### Workflow Steps

1. **Create a new branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write clean, readable code
   - Follow Django and DRF best practices
   - Add tests for new functionality
   - Update documentation if needed

3. **Run tests and linting**
   ```bash
   # Run tests
   pytest
   
   # Check code style
   flake8
   
   # Format code
   black .
   isort .
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add event tagging functionality"
   ```

5. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request**
   - Go to GitHub and create a PR
   - Fill in the PR template
   - Link related issues

## Coding Standards

### Python Style Guide

- Follow **PEP 8** style guide
- Use **Black** for code formatting (line length: 88)
- Use **isort** for import sorting
- Maximum line length: 88 characters
- Use type hints where appropriate

### Django Best Practices

- **Models**: Business logic in models
- **Views**: Use DRF ViewSets for APIs
- **Serializers**: Separate serializers for read/write operations
- **Permissions**: Custom permission classes when needed
- **Query Optimization**: Always use `select_related` and `prefetch_related`

### Code Examples

**Good:**
```python
class EventViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Event management with optimized queries.
    """
    queryset = Event.objects.select_related('organizer').all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOrganizerOrReadOnly]
    
    def get_queryset(self):
        """Filter events based on user access."""
        user = self.request.user
        if not user.is_authenticated:
            return self.queryset.filter(is_public=True)
        return self.queryset.filter(
            Q(is_public=True) | Q(organizer=user)
        ).distinct()
```

**Bad:**
```python
class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()  # N+1 queries!
    serializer_class = EventSerializer
    # No permission checks!
```

### Testing Standards

- Write tests for all new features
- Minimum 80% code coverage
- Test happy paths and edge cases
- Use pytest fixtures for common setups

```python
@pytest.mark.django_db
class TestEventAPI:
    def test_create_event_authenticated(self, api_client, user):
        """Test authenticated user can create event."""
        api_client.force_authenticate(user=user)
        response = api_client.post('/api/events/', {
            'title': 'Test Event',
            'description': 'Test Description',
            'location': 'Test Location',
            'start_time': '2025-12-01T10:00:00Z',
            'end_time': '2025-12-01T12:00:00Z',
        })
        assert response.status_code == 201
```

### Commit Message Convention

Follow **Conventional Commits** specification:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```bash
feat(events): add event tagging functionality
fix(rsvp): resolve duplicate RSVP issue
docs(api): update API documentation for reviews endpoint
test(events): add comprehensive event creation tests
refactor(views): optimize query performance with select_related
```

## Submitting Changes

### Pull Request Process

1. **Update documentation** if you've changed APIs
2. **Add tests** for new functionality
3. **Ensure all tests pass**
4. **Update CHANGELOG.md** with your changes
5. **Fill out the PR template** completely

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] Added new tests for changes
- [ ] Updated existing tests

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings generated
```

### Code Review Process

- At least one approving review required
- All automated checks must pass
- Address all review comments
- Maintain respectful discussion

## Reporting Bugs

### Before Submitting a Bug Report

1. **Check existing issues** - someone might have reported it already
2. **Update to latest version** - bug might be fixed
3. **Collect debugging information**

### Bug Report Template

```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce:
1. Go to '...'
2. Click on '....'
3. See error

**Expected behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment:**
- OS: [e.g., Windows 11, Ubuntu 22.04]
- Python version: [e.g., 3.11.4]
- Django version: [e.g., 4.2.7]
- Browser: [if applicable]

**Additional context**
Any other relevant information.
```

## Suggesting Features

### Feature Request Template

```markdown
**Is your feature request related to a problem?**
A clear description of the problem.

**Describe the solution you'd like**
Clear description of what you want to happen.

**Describe alternatives you've considered**
Other solutions or features you've considered.

**Additional context**
Any other context, mockups, or examples.
```

## Development Tips

### Running Specific Tests
```bash
# Run specific test file
pytest events/tests.py -v

# Run specific test class
pytest events/tests.py::EventAPITest -v

# Run with coverage
pytest --cov=events --cov-report=html
```

### Database Management
```bash
# Create new migration
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Rollback migration
python manage.py migrate events 0001_initial

# Reset database (development only!)
python manage.py flush
```

### Docker Development
```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f web

# Run commands in container
docker-compose exec web python manage.py migrate

# Stop services
docker-compose down
```

## Questions?

Feel free to:
- Open an issue for questions
- Join our discussions
- Reach out to maintainers

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT License).

---

Thank you for contributing! 🙏
