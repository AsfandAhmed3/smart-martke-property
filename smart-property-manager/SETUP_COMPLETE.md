# Smart Real Estate Portfolio Management System - Setup Guide

## Overview
This system is now fully connected to Supabase PostgreSQL database with superadmin functionality and real-time data integration.

## What's Been Implemented

### ✅ Database Connection
- **Supabase PostgreSQL** connected and configured
- Database credentials stored securely in `.env` file
- All models migrated to PostgreSQL

### ✅ User Authentication & Authorization
- **Real user data** displayed in header (no more hardcoded "Jack")
- User's full name shown in top-right corner
- User initials displayed in avatar
- JWT-based authentication

### ✅ Superadmin Functionality
- `is_superadmin` field added to User model
- Superadmin can access User Management page
- **User Management Features:**
  - View all users with search and filters
  - Create new users
  - Edit existing users
  - Toggle superadmin privileges
  - Delete users
  - View user statistics
  - Filter by role, status, and superadmin status

### ✅ Real Data Integration
- All backend views use **real database queries**
- Dashboard statistics pull from actual data
- Properties, tenants, leases, financials, maintenance - all functional with real data
- Notifications system connected to real events via Django signals

### ✅ Admin Features
- User management page (`/admin/users`) for superadmins only
- Role-based access control (RBAC)
- Permission system integrated
- User statistics dashboard

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 16+
- PostgreSQL client (psycopg2)

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Set up environment variables:**
   ```bash
   # Copy the example .env file
   cp .env.example .env
   
   # Edit .env and add your Supabase credentials:
   # DB_USER=your-supabase-user
   # DB_PASSWORD=your-supabase-password
   # DB_HOST=your-supabase-host.supabase.com
   ```

3. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superadmin user:**
   ```bash
   python manage.py create_superadmin
   ```
   
   Or with custom credentials:
   ```bash
   python manage.py create_superadmin --email=admin@example.com --password=YourPassword123 --first-name=John --last-name=Doe
   ```

6. **Start the development server:**
   ```bash
   python manage.py runserver
   ```
   Backend will run on `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm run dev
   ```
   Frontend will run on `http://localhost:5173`

### Quick Setup (PowerShell)

Run the provided setup script:
```powershell
.\setup.ps1
```

## Accessing the System

1. **Login:** Navigate to `http://localhost:5173/login`
2. **Superadmin Credentials:**
   - Email: `admin@smartproperty.com` (or your custom email)
   - Password: `admin123456` (or your custom password)

3. **After Login:**
   - Your name will appear in the top-right corner
   - Superadmins will see "User Management" in the sidebar

## Key Features

### For All Users
- Dashboard with real-time statistics
- Property management
- Tenant CRM
- Lease management
- Financial tracking
- Maintenance requests
- Document management
- Notifications

### For Superadmins Only
- **User Management** (`/admin/users`)
  - Create/Edit/Delete users
  - Assign roles
  - Grant/Revoke superadmin privileges
  - View user statistics
  - Search and filter users

## Database Schema

### Key Models
- **User** - Extended Django user with roles and superadmin flag
- **Role** - RBAC roles with permissions
- **Property** - Real estate properties
- **Tenant** - Tenant information
- **Lease** - Lease agreements
- **Payment** - Financial transactions
- **MaintenanceRequest** - Maintenance tracking
- **Notification** - User notifications
- **Document** - File storage metadata

## API Endpoints

### Authentication
- `POST /api/auth/login/` - User login
- `POST /api/auth/register/` - User registration
- `POST /api/auth/logout/` - User logout
- `GET /api/auth/profile/` - Get user profile

### Admin (Superadmin Only)
- `GET /api/auth/admin/users/` - List all users
- `POST /api/auth/admin/users/create/` - Create user
- `GET /api/auth/admin/users/{id}/` - Get user details
- `PATCH /api/auth/admin/users/{id}/` - Update user
- `DELETE /api/auth/admin/users/{id}/` - Delete user
- `POST /api/auth/admin/users/{id}/toggle-superadmin/` - Toggle superadmin
- `GET /api/auth/admin/users/stats/` - User statistics

### Properties
- `GET /api/properties/` - List properties
- `POST /api/properties/` - Create property
- `GET /api/properties/{id}/` - Get property
- `PATCH /api/properties/{id}/` - Update property
- `DELETE /api/properties/{id}/` - Delete property

## Notifications System

Notifications are automatically created for:
- Lease expiring soon (30 days)
- Payment due/overdue
- Payment received
- New maintenance requests
- Maintenance completed
- New documents uploaded
- Reports ready

## Security Features

- JWT authentication with token refresh
- Role-based access control (RBAC)
- Superadmin-only routes protected
- Password validation
- CORS configuration
- Encrypted database connection (SSL)

## What's NOT Yet Implemented

As per your requirements, the following are excluded for now:
- ROI prediction model
- Google Maps integration
- AWS services (S3, Lambda)

These will be implemented later as specified.

## Troubleshooting

### Database Connection Issues
- Verify Supabase credentials
- Check network connectivity
- Ensure SSL is enabled

### Migration Errors
```bash
python manage.py makemigrations --empty users
python manage.py migrate --fake-initial
```

### Frontend Not Connecting to Backend
- Verify backend is running on port 8000
- Check CORS settings in `backend/config/settings.py`
- Ensure API_URL in `frontend/src/services/api.js` is correct

## Development Notes

- Backend uses Django REST Framework
- Frontend uses Vue 3 with Composition API
- State management with Pinia
- Database: Supabase PostgreSQL
- Authentication: JWT tokens

## Next Steps

1. ✅ Connect Supabase - DONE
2. ✅ Display real user name - DONE
3. ✅ Create superadmin - DONE
4. ✅ User management page - DONE
5. ✅ Real data integration - DONE
6. 🔄 Test all functionality
7. ⏳ Implement ROI model (later)
8. ⏳ Integrate maps (later)
9. ⏳ Setup AWS services (later)

## Support

For issues or questions, contact the development team.
