---
name: 🐛 Bug Report
about: Create a report to help us improve
title: '[BUG] '
labels: bug
assignees: ''
---

## Bug Description

<!-- A clear and concise description of what the bug is -->

## Steps to Reproduce

<!-- Steps to reproduce the behavior -->

1. Go to '...'
2. Click on '...'
3. Scroll down to '...'
4. See error

## Expected Behavior

<!-- A clear and concise description of what you expected to happen -->

## Actual Behavior

<!-- A clear and concise description of what actually happened -->

## Error Messages

<!-- If applicable, paste any error messages -->

```
Paste error messages here
```

## Screenshots

<!-- If applicable, add screenshots to help explain your problem -->

## Environment

<!-- Please complete the following information -->

- **OS**: [e.g., Windows 10, Ubuntu 22.04, macOS 13]
- **Python Version**: [e.g., 3.11.4]
- **Django Version**: [e.g., 4.2.7]
- **Browser** (if applicable): [e.g., Chrome 120, Firefox 121]
- **Database**: [e.g., PostgreSQL 15, SQLite 3]

## API Request Details (if applicable)

**Endpoint**: 
```
POST /api/events/
```

**Request Headers**:
```json
{
  "Authorization": "Bearer eyJ...",
  "Content-Type": "application/json"
}
```

**Request Body**:
```json
{
  "title": "Test Event",
  "description": "Test Description"
}
```

**Response**:
```json
{
  "error": "Error message"
}
```

## Logs

<!-- Paste relevant logs from Django, Celery, or Redis -->

**Django logs**:
```
[timestamp] ERROR: ...
```

**Celery logs**:
```
[timestamp] ERROR: ...
```

## Database State (if applicable)

<!-- Describe any relevant database state -->

- Number of Events: X
- Number of Users: Y
- Recent migrations applied: Z

## Additional Context

<!-- Add any other context about the problem here -->

## Possible Solution

<!-- If you have ideas on how to fix the bug, describe them here -->

## Related Issues

<!-- Link to related issues -->

- Related to #(issue number)

## Checklist

- [ ] I have searched for similar issues
- [ ] I am using the latest version
- [ ] I have provided all required information
- [ ] I have included error messages and logs
- [ ] I have described steps to reproduce
