# 🚀 Quick Start Guide

## Prerequisites
- Python 3.9+
- Node.js 16+
- Git

## Installation

### 1. Backend Setup (Django)

```powershell
# Navigate to backend directory
cd "c:\personal\Client project\market\smart-property-manager\backend"

# Virtual environment is already created, just activate it
.\venv\Scripts\activate

# Install remaining dependencies (if needed)
pip install -r requirements.txt

# Database is already migrated and seeded
# If you need to reset the database, run:
# python manage.py migrate
# python manage.py seed_data
```

### 2. Frontend Setup (Vue.js)

```powershell
# Navigate to frontend directory
cd "c:\personal\Client project\market\smart-property-manager\frontend"

# Dependencies are already installed
# If you need to reinstall:
# npm install
```

## Running the Application

### Start Backend (Terminal 1)
```powershell
cd "c:\personal\Client project\market\smart-property-manager\backend"
.\venv\Scripts\activate
python manage.py runserver
```
✅ Backend running at: http://127.0.0.1:8000/

### Start Frontend (Terminal 2)
```powershell
cd "c:\personal\Client project\market\smart-property-manager\frontend"
npm run dev
```
✅ Frontend running at: http://localhost:5173/

## Access the Application

1. Open browser to http://localhost:5173/
2. You'll see the login page
3. Login with demo credentials:
   - **Email**: jack@gmail.com
   - **Password**: password
4. You'll be redirected to the Dashboard

## API Endpoints

Base URL: http://127.0.0.1:8000/api/

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login (returns JWT tokens)
- `POST /api/auth/logout/` - Logout
- `POST /api/auth/token/refresh/` - Refresh access token
- `GET /api/auth/profile/` - Get user profile
- `PATCH /api/auth/profile/` - Update user profile
- `POST /api/auth/change-password/` - Change password
- `GET /api/auth/roles/` - List all roles

### Test API with curl

```powershell
# Login
curl -X POST http://127.0.0.1:8000/api/auth/login/ `
  -H "Content-Type: application/json" `
  -d '{\"email\":\"jack@gmail.com\",\"password\":\"password\"}'

# Get profile (replace TOKEN with access token from login)
curl -X GET http://127.0.0.1:8000/api/auth/profile/ `
  -H "Authorization: Bearer TOKEN"
```

## Project Structure

```
smart-property-manager/
├── backend/                    # Django Backend
│   ├── config/                # Django settings & URLs
│   ├── users/                 # Authentication & RBAC
│   ├── properties/            # Property management (TODO)
│   ├── tenants/               # Tenant CRM (TODO)
│   ├── leases/                # Lease management (TODO)
│   ├── financials/            # Financial tracking (TODO)
│   ├── manage.py
│   └── db.sqlite3            # SQLite database
│
├── frontend/                   # Vue.js Frontend
│   ├── src/
│   │   ├── assets/           # Styles (styles.css)
│   │   ├── layouts/          # DashboardLayout.vue
│   │   ├── router/           # index.js (Vue Router)
│   │   ├── services/         # api.js (Axios client)
│   │   ├── stores/           # auth.js (Pinia store)
│   │   ├── views/            # Login.vue, Dashboard.vue, etc.
│   │   ├── App.vue
│   │   └── main.js
│   ├── package.json
│   └── vite.config.js
│
├── README.md
├── PROJECT_STATUS.md          # Current status & next steps
└── QUICK_START.md            # This file
```

## Demo Users

### Portfolio Manager (Regular User)
- **Email**: jack@gmail.com
- **Password**: password
- **Role**: Portfolio Manager
- **Permissions**: Can manage properties, tenants, leases, financials

### Administrator
- **Email**: admin@smartproperty.com
- **Password**: admin123
- **Role**: Admin
- **Permissions**: Full system access including user management

## Development Workflow

### Adding New Features

1. **Backend**: Create Django models, serializers, views in respective apps
2. **Frontend**: Create Vue components in `src/views/` or `src/components/`
3. **API Integration**: Add API calls to `src/services/api.js`
4. **Routing**: Add routes to `src/router/index.js`

### Database Changes

```powershell
cd backend
.\venv\Scripts\activate

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

### Installing New Packages

**Backend:**
```powershell
cd backend
.\venv\Scripts\activate
pip install package-name
pip freeze > requirements.txt
```

**Frontend:**
```powershell
cd frontend
npm install package-name
```

## Troubleshooting

### Port Already in Use

**Backend (8000):**
```powershell
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID)
taskkill /PID <PID> /F
```

**Frontend (5173):**
```powershell
# Find process using port 5173
netstat -ano | findstr :5173

# Kill the process
taskkill /PID <PID> /F
```

### CORS Errors

Make sure Django backend is running and CORS settings in `config/settings.py` include:
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
```

### Database Reset

```powershell
cd backend
.\venv\Scripts\activate

# Delete database
del db.sqlite3

# Recreate and migrate
python manage.py migrate

# Seed demo data
python manage.py seed_data
```

## Next Steps

See `PROJECT_STATUS.md` for:
- ✅ Completed features
- 🔄 In-progress features
- 📋 Planned features

The current focus is on building the Properties page with property cards and map integration according to the Figma design.

## Support

For issues or questions about the project:
1. Check `PROJECT_STATUS.md` for current status
2. Review Figma file: `Smart Property Manager.fig`
3. Verify both servers are running
4. Check browser console for frontend errors
5. Check Django terminal for backend errors

---

**Happy Coding! 🎉**
