# 🚀 GET STARTED IN 5 MINUTES

## For Users Who Just Want to Try It

### Option 1: Automated Setup (Easiest)

**Windows:**
```bash
setup.bat
```

**Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

Then:
```bash
# Create sample data
python manage.py create_sample_data

# Run server
python manage.py runserver
```

✅ **Done!** Visit http://127.0.0.1:8000/api/

Test users available:
- **Username**: user1, user2, user3, user4, user5
- **Password**: password123

---

### Option 2: Docker (Super Easy)

```bash
docker-compose up
```

✅ **Done!** Visit http://127.0.0.1:8000/api/

---

### Option 3: Manual Setup (5 Steps)

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate it
venv\Scripts\activate          # Windows
source venv/bin/activate       # Linux/Mac

# 3. Install packages
pip install -r requirements.txt

# 4. Setup database
python manage.py migrate

# 5. Run server
python manage.py runserver
```

---

## Quick Test

### 1. Get a JWT Token

```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"user1","password":"password123"}'
```

**Save the `access` token from the response.**

### 2. Create Your First Event

```bash
curl -X POST http://127.0.0.1:8000/api/events/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My First Event",
    "description": "Testing the API",
    "location": "Online",
    "start_time": "2025-12-01T10:00:00Z",
    "end_time": "2025-12-01T12:00:00Z",
    "is_public": true
  }'
```

### 3. View All Events

```bash
curl http://127.0.0.1:8000/api/events/
```

### 4. RSVP to an Event

```bash
curl -X POST http://127.0.0.1:8000/api/events/1/rsvp/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status": "going"}'
```

---

## What's Next?

### Explore the API
- 📖 Read `API_USAGE.md` for all endpoints
- 🔍 Try `QUICK_REFERENCE.md` for command cheat sheet
- 📚 Check `README.md` for full documentation

### For Developers
- 👨‍💻 Read `DEVELOPMENT.md` for development guide
- 🧪 Run tests: `pytest`
- 🐳 Use Docker: `docker-compose up`

### Admin Panel
Visit http://127.0.0.1:8000/admin/

Create admin:
```bash
python manage.py createsuperuser
```

### Enable Email Notifications (Optional)

Start Redis and Celery:
```bash
# Terminal 1
redis-server

# Terminal 2
celery -A event_management worker -l info
```

---

## File Guide

| File | Purpose |
|------|---------|
| `README.md` | 📚 Complete documentation |
| `QUICK_REFERENCE.md` | ⚡ Command cheat sheet |
| `API_USAGE.md` | 🔌 API examples (curl, Python, JS) |
| `DEVELOPMENT.md` | 👨‍💻 Developer guide |
| `PROJECT_SUMMARY.md` | 📊 Project overview |
| `FEATURES.md` | ✨ Complete feature list |
| `setup.bat` / `setup.sh` | 🚀 Automated setup scripts |
| `docker-compose.yml` | 🐳 Docker setup |

---

## Troubleshooting

**Error: Module not found**
```bash
pip install -r requirements.txt
```

**Error: No migrations**
```bash
python manage.py migrate
```

**Error: Redis connection refused**
```bash
redis-server
```

**Error: Permission denied**
- Check you're using the correct JWT token
- Ensure token is in the format: `Bearer <token>`

---

## Need Help?

1. Check `README.md` for detailed docs
2. See `DEVELOPMENT.md` for troubleshooting
3. Review test files in `events/tests.py` for examples
4. Check the assignment spec: `PYTHONIIP01010.md`

---

## Summary

✅ **Full REST API** for event management  
✅ **JWT Authentication** with token refresh  
✅ **RSVP & Review System** with validation  
✅ **Custom Permissions** for access control  
✅ **Query Optimization** with caching  
✅ **Async Notifications** via Celery  
✅ **Comprehensive Tests** with pytest  
✅ **Docker Support** for easy deployment  
✅ **Complete Documentation** with examples  

**You're all set! 🎉**

Start the server and explore the API!
