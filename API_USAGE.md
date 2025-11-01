# API Usage Guide

## Quick Start with curl

### 1. Create a User (Admin Panel or Django Shell)

```bash
# Using Django shell
python manage.py shell

from django.contrib.auth.models import User
user = User.objects.create_user('john', 'john@example.com', 'password123')
```

### 2. Get JWT Token

```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "john", "password": "password123"}'
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

Save the `access` token for subsequent requests.

### 3. Create an Event

```bash
curl -X POST http://127.0.0.1:8000/api/events/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Django Conference 2025",
    "description": "Annual Django developers conference",
    "location": "Convention Center, San Francisco",
    "start_time": "2025-12-01T09:00:00Z",
    "end_time": "2025-12-01T18:00:00Z",
    "is_public": true
  }'
```

### 4. List All Public Events

```bash
curl http://127.0.0.1:8000/api/events/
```

### 5. Get Event Details

```bash
curl http://127.0.0.1:8000/api/events/1/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 6. Update Your Event

```bash
curl -X PATCH http://127.0.0.1:8000/api/events/1/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Django Conference 2025 - Updated"}'
```

### 7. RSVP to an Event

```bash
curl -X POST http://127.0.0.1:8000/api/events/1/rsvp/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status": "going"}'
```

### 8. Update RSVP Status

```bash
curl -X PATCH http://127.0.0.1:8000/api/rsvps/1/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status": "maybe"}'
```

### 9. Add a Review

```bash
curl -X POST http://127.0.0.1:8000/api/events/1/review/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "rating": 5,
    "comment": "Excellent event! Very well organized."
  }'
```

### 10. List Event Reviews

```bash
curl http://127.0.0.1:8000/api/events/1/reviews/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 11. Search Events

```bash
# Search by title
curl "http://127.0.0.1:8000/api/events/?search=django"

# Filter by location
curl "http://127.0.0.1:8000/api/events/?location=San%20Francisco"

# Filter by organizer
curl "http://127.0.0.1:8000/api/events/?organizer=1"

# Combine filters
curl "http://127.0.0.1:8000/api/events/?search=conference&is_public=true"
```

### 12. Update User Profile

```bash
curl -X PATCH http://127.0.0.1:8000/api/profile/me/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "John Doe",
    "bio": "Django enthusiast and backend developer",
    "location": "San Francisco, CA"
  }'
```

### 13. Delete an Event (Organizer Only)

```bash
curl -X DELETE http://127.0.0.1:8000/api/events/1/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Python Requests Examples

```python
import requests

BASE_URL = "http://127.0.0.1:8000/api"

# Get token
response = requests.post(f"{BASE_URL}/token/", json={
    "username": "john",
    "password": "password123"
})
token = response.json()["access"]

# Set headers
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# Create event
event_data = {
    "title": "Python Meetup",
    "description": "Monthly Python developers meetup",
    "location": "Tech Hub",
    "start_time": "2025-11-15T18:00:00Z",
    "end_time": "2025-11-15T21:00:00Z",
    "is_public": True
}
response = requests.post(f"{BASE_URL}/events/", json=event_data, headers=headers)
event = response.json()

# RSVP to event
response = requests.post(
    f"{BASE_URL}/events/{event['id']}/rsvp/",
    json={"status": "going"},
    headers=headers
)

# Add review
response = requests.post(
    f"{BASE_URL}/events/{event['id']}/review/",
    json={"rating": 5, "comment": "Great meetup!"},
    headers=headers
)
```

## JavaScript/Fetch Examples

```javascript
const BASE_URL = "http://127.0.0.1:8000/api";

// Get token
async function getToken() {
  const response = await fetch(`${BASE_URL}/token/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      username: 'john',
      password: 'password123'
    })
  });
  const data = await response.json();
  return data.access;
}

// Create event
async function createEvent(token) {
  const response = await fetch(`${BASE_URL}/events/`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      title: "JavaScript Workshop",
      description: "Learn modern JavaScript",
      location: "Online",
      start_time: "2025-11-20T14:00:00Z",
      end_time: "2025-11-20T17:00:00Z",
      is_public: true
    })
  });
  return await response.json();
}

// RSVP to event
async function rsvpToEvent(token, eventId) {
  const response = await fetch(`${BASE_URL}/events/${eventId}/rsvp/`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ status: 'going' })
  });
  return await response.json();
}
```

## Common Response Codes

- `200 OK` - Successful GET, PUT, PATCH requests
- `201 Created` - Successful POST request
- `204 No Content` - Successful DELETE request
- `400 Bad Request` - Invalid data or validation error
- `401 Unauthorized` - Missing or invalid authentication token
- `403 Forbidden` - Permission denied
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

## Pagination

List endpoints return paginated results:

```json
{
  "count": 42,
  "next": "http://127.0.0.1:8000/api/events/?page=2",
  "previous": null,
  "results": [...]
}
```

Access different pages:
```bash
curl "http://127.0.0.1:8000/api/events/?page=2"
```

## Error Responses

Validation errors return detailed information:

```json
{
  "field_name": [
    "Error message 1",
    "Error message 2"
  ]
}
```

Example:
```json
{
  "end_time": [
    "End time must be after start time."
  ]
}
```
