# Security Policy

## Supported Versions

Currently supported versions with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

**Please do NOT report security vulnerabilities through public GitHub issues.**

If you discover a security vulnerability, please follow these steps:

### 1. Email Security Team

Send details to: **pushkarmodi111@gmail.com**

Include the following in your report:

- **Type of vulnerability**: [e.g., SQL Injection, XSS, CSRF]
- **Full paths of affected file(s)**
- **Location of the affected source code** (tag/branch/commit or direct URL)
- **Step-by-step instructions to reproduce the issue**
- **Proof-of-concept or exploit code** (if possible)
- **Impact of the issue** (what an attacker could do)
- **Suggested fix** (if you have one)

### 2. What to Expect

- **Initial Response**: Within 48 hours
- **Status Update**: Within 7 days
- **Resolution Timeline**: Varies based on complexity

### 3. Response Process

1. **Acknowledgment**: We'll confirm receipt of your report
2. **Investigation**: We'll investigate and validate the issue
3. **Fix Development**: We'll develop and test a fix
4. **Disclosure**: We'll coordinate disclosure timeline with you
5. **Credit**: We'll credit you in the security advisory (if desired)

## Security Best Practices

### For Contributors

- Never commit sensitive data (passwords, API keys, tokens)
- Use environment variables for configuration
- Follow OWASP Top 10 guidelines
- Implement proper input validation
- Use parameterized queries (ORM)
- Enable CSRF protection
- Implement rate limiting
- Use HTTPS in production
- Keep dependencies updated

### For Deployers

#### Environment Variables

Always set these in production:

```bash
SECRET_KEY=<strong-random-key>
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
DATABASE_URL=postgresql://...
REDIS_URL=redis://...
```

#### Security Headers

Ensure these settings in `settings.py`:

```python
# HTTPS
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Headers
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
```

#### Database Security

```python
# Use strong passwords
DATABASES = {
    'default': {
        'PASSWORD': os.environ['DB_PASSWORD'],  # Never hardcode
    }
}

# Enable SSL for database connections
DATABASES['default']['OPTIONS'] = {
    'sslmode': 'require',
}
```

#### CORS Configuration

```python
# Be specific with CORS origins
CORS_ALLOWED_ORIGINS = [
    "https://yourdomain.com",
]

# Don't use wildcard in production
CORS_ALLOW_ALL_ORIGINS = False
```

## Known Security Considerations

### JWT Token Security

- **Token Storage**: Store JWT tokens securely (HttpOnly cookies or secure storage)
- **Token Expiration**: Access tokens expire in 60 minutes, refresh in 1 day
- **Token Rotation**: Implement token rotation on refresh
- **Revocation**: Consider implementing token blacklisting

### API Security

- **Authentication**: All endpoints require JWT authentication
- **Authorization**: Permission classes enforce access control
- **Rate Limiting**: Implement rate limiting to prevent abuse
- **Input Validation**: All inputs validated through DRF serializers

### Database Security

- **ORM Usage**: Using Django ORM prevents SQL injection
- **Migrations**: Review migrations for security implications
- **Backups**: Regular backups with encryption

### File Upload Security

If implementing file uploads:

- Validate file types and sizes
- Scan for malware
- Store files outside web root
- Use unique filenames
- Implement access controls

### Celery Task Security

- **Task Validation**: Validate task inputs
- **Result Backend**: Secure Redis connection
- **Task Routing**: Use dedicated queues for sensitive tasks

## Security Checklist for Releases

Before each release, verify:

- [ ] Dependencies updated and scanned
- [ ] Security tests passing
- [ ] Static security analysis (Bandit) clean
- [ ] No hardcoded secrets in code
- [ ] Environment variable documentation complete
- [ ] Security headers configured
- [ ] HTTPS enforced
- [ ] Database backups configured
- [ ] Rate limiting implemented
- [ ] Error messages don't leak sensitive info

## Security Tools

### CI/CD Security Checks

Our GitHub Actions workflow runs:

- **Safety**: Checks for known security vulnerabilities in dependencies
- **Bandit**: Static analysis security testing for Python
- **Dependency Review**: GitHub's dependency scanning

### Manual Security Testing

Recommended tools:

```bash
# Dependency vulnerabilities
pip install safety
safety check

# Code security
pip install bandit
bandit -r . -f json -o bandit-report.json

# Django security checks
python manage.py check --deploy
```

## Vulnerability Disclosure Policy

### Timeline

- **Day 0**: Vulnerability reported
- **Day 1-2**: Acknowledgment sent
- **Day 3-7**: Initial assessment
- **Day 7-30**: Fix developed and tested
- **Day 30**: Patch released
- **Day 37**: Public disclosure (7 days after patch)

### Exceptions

Critical vulnerabilities may be handled faster.

## Hall of Fame

We appreciate security researchers who help improve our security:

<!-- Security researchers will be listed here -->

## Contact

- **Security Issues**: pushkarmodi111@gmail.com
- **General Issues**: GitHub Issues
- **Project Maintainer**: Pushkar Modi

## Updates

This security policy was last updated: **January 2025**

---

Thank you for helping keep this project secure! 🔒
