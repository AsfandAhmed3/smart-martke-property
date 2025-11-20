# Smart Real Estate Portfolio Management System - Project Documentation

## 🎯 Project Overview

A comprehensive real estate portfolio management system built with Django backend and Vue.js frontend, featuring role-based access control, property management, tenant CRM, lease tracking, financial analytics, and AI-powered insights.

## 🏗️ Architecture

### Backend (Django 4.2.26)
- **Framework**: Django REST Framework 3.16.1
- **Authentication**: JWT (djangorestframework-simplejwt 5.5.1)
- **Database**: SQLite
- **Port**: 8000

### Frontend (Vue 3 + Vite)
- **Framework**: Vue 3 with Composition API
- **Build Tool**: Vite 7.2.2
- **Router**: Vue Router 4.x
- **State Management**: Pinia
- **HTTP Client**: Axios with interceptors
- **Port**: 5173

## 🎨 Design System

### Color Palette
- **Primary Purple**: #7C6FDC, #9B8FE8 (Gradient)
- **Action Blue**: #3B82F6
- **Success Green**: #10B981
- **Warning Yellow**: #F59E0B
- **Error Red**: #EF4444
- **Neutral Grays**: #F9FAFB, #E5E7EB, #6B7280, #374151, #1A1A1A

### Typography
- **Font Family**: 'Inter', sans-serif
- **Heading Weights**: 600-700
- **Body Weight**: 400-500

## 👥 Authentication & Authorization

### User Roles
1. **Admin**
   - Full system access
   - User management
   - All CRUD operations

2. **Portfolio Manager**
   - Property management
   - Tenant/lease management
   - Financial analytics
   - Report generation

3. **Property Owner**
   - View-only access to owned properties
   - Basic analytics
   - Document access

### Demo Credentials
```
Portfolio Manager:
Email: jack@gmail.com
Password: password

Admin:
Email: admin@smartproperty.com
Password: admin123
```

## 📦 Core Features

### 1. Authentication System
- ✅ JWT-based login
- ✅ User registration with auto-login
- ✅ Token refresh on 401 errors
- ✅ Persistent sessions (localStorage)
- ✅ Logout functionality

### 2. Dashboard
- ✅ KPI Cards (Total Revenue, Properties, Occupancy Rate, Monthly Income)
- ✅ Recent Activity Feed
- ✅ Quick Actions
- ✅ Property Performance Overview

### 3. Properties Management
- ✅ Property listing with cards
- ✅ Map placeholder for location view
- ✅ Property details (name, location, units, occupancy)
- ✅ Financial metrics (revenue, value, ROI)
- ✅ Add Property Modal with form validation

### 4. Tenant CRM
- ✅ Tenant cards with avatars (initials)
- ✅ Contact information (email, phone)
- ✅ Lease details (property, unit, rent)
- ✅ Status badges (Active/Inactive)
- ✅ Search and filter functionality
- ✅ Add Tenant Modal (Personal Info, Employment, Rental Info)

### 5. Lease Management
- ✅ Statistics dashboard (Total, Active, Expiring, Expired)
- ✅ Lease table view
- ✅ Tenant information with avatars
- ✅ Property and unit details
- ✅ Date tracking (start/end dates)
- ✅ Status indicators
- ✅ Create Lease Modal with terms and payment info

### 6. Analytics & ROI
- ✅ Financial KPI cards (Revenue, ROI, Occupancy, NOI)
- ✅ Chart placeholders (Revenue Trend, Performance)
- ✅ Property performance breakdown
- ✅ ROI badges (High/Medium/Low)
- ✅ Generate Report Modal with configuration options

### 7. Maintenance Requests
- ✅ Status overview (Open, In Progress, Completed)
- ✅ Request cards with details
- ✅ Priority badges (High, Medium, Low)
- ✅ Status indicators
- ✅ Assignment tracking
- ✅ Request date display

### 8. AI Insights
- ✅ Featured insight card
- ✅ Multiple insight categories
- ✅ Recommendations section
- ✅ Priority indicators
- ✅ AI Lead Generation Modal with results display

### 9. Documents Repository
- ✅ Document statistics (Total, Folders, Storage)
- ✅ Folder cards with counts
- ✅ Recent documents list
- ✅ File type icons (PDF, DOCX, XLSX, JPG)
- ✅ Date tracking

### 10. Profile Management
- ✅ Profile dropdown menu (View Profile, Account Settings, Logout)
- ✅ View Profile page with comprehensive user information
- ✅ Account Settings page with 6 sections
- ✅ Edit profile functionality

## 🔧 Account Settings Features

### Change Password
- Current password validation
- New password requirements (min 8 characters)
- Password confirmation matching
- Success/error messaging

### Notification Preferences
- Email notifications toggle
- Lease reminders toggle
- Maintenance alerts toggle
- Payment notifications toggle

### Two-Factor Authentication
- Enable/disable MFA
- Status badge display
- Security description

### API Access Keys
- List of generated keys
- Masked key display
- Generate new key functionality
- Delete key functionality
- Creation date tracking

### Billing Information
- Current plan display
- Billing cycle information
- Next billing date
- Amount display
- Update payment method button

### Data Export
- Export as JSON
- Export as CSV
- Export as Excel
- Format selection buttons

## 👤 View Profile Features

### Profile Header
- Large profile avatar with initials
- Change photo button
- Full name display
- Role badge
- Email address
- Member since date
- Edit profile button

### Personal Information Section
- First Name
- Last Name
- Username
- Email Address
- Phone Number
- Date of Birth

### Account Details Section
- Role with badge
- Account status (Active/Inactive)
- Member since date
- Last login date
- Two-factor auth status
- Email verification status

### Role Permissions Display
- Visual permission grid
- Checkmarks for granted permissions
- X marks for denied permissions
- 9 permission types:
  - Create Properties
  - Edit Properties
  - Delete Properties
  - Manage Tenants
  - Manage Leases
  - Manage Financials
  - Manage Users
  - View Analytics
  - Export Reports

### Activity Statistics
- Properties Managed (with icon)
- Total Tenants (with icon)
- Active Leases (with icon)
- Monthly Revenue (with icon)

### Edit Profile Modal
- First Name field
- Last Name field
- Email field
- Phone field
- Date of Birth field
- Save/Cancel buttons
- Form validation
- Loading states

## 📁 Project Structure

```
smart-property-manager/
├── backend/
│   ├── manage.py
│   ├── backend/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── users/
│   │   ├── models.py (User, Role)
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── properties/
│   │   ├── models.py (Property, Owner)
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── tenants/
│   ├── leases/
│   └── financials/
├── frontend/
│   ├── src/
│   │   ├── assets/
│   │   │   └── main.css
│   │   ├── components/
│   │   │   ├── AddPropertyModal.vue
│   │   │   ├── AddTenantModal.vue
│   │   │   ├── CreateLeaseModal.vue
│   │   │   ├── GenerateReportModal.vue
│   │   │   └── AILeadGenerationModal.vue
│   │   ├── layouts/
│   │   │   └── DashboardLayout.vue
│   │   ├── views/
│   │   │   ├── Login.vue
│   │   │   ├── Register.vue
│   │   │   ├── Dashboard.vue
│   │   │   ├── Properties.vue
│   │   │   ├── Tenants.vue
│   │   │   ├── Leases.vue
│   │   │   ├── Analytics.vue
│   │   │   ├── Maintenance.vue
│   │   │   ├── AIInsights.vue
│   │   │   ├── Documents.vue
│   │   │   ├── ViewProfile.vue
│   │   │   └── AccountSettings.vue
│   │   ├── stores/
│   │   │   └── auth.js
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── router/
│   │   │   └── index.js
│   │   ├── App.vue
│   │   └── main.js
│   ├── package.json
│   └── vite.config.js
└── requirements.txt
```

## 🚀 Running the Application

### Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata users/fixtures/roles.json
python manage.py loaddata users/fixtures/users.json
python manage.py loaddata properties/fixtures/properties.json
python manage.py runserver
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Access the Application
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin

## 🔐 API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/token/refresh/` - Refresh access token
- `POST /api/auth/logout/` - User logout

### Users
- `GET /api/users/me/` - Get current user details

### Properties
- `GET /api/properties/` - List all properties
- `POST /api/properties/` - Create new property
- `GET /api/properties/{id}/` - Get property details
- `PUT /api/properties/{id}/` - Update property
- `DELETE /api/properties/{id}/` - Delete property

## 🎯 Component Features

### Modal Components
All modals include:
- Backdrop overlay with click-outside to close
- Close button (X icon)
- Form validation
- Loading states
- Success/error handling
- Consistent styling
- Responsive design

### Page Components
All pages include:
- Consistent header sections
- Search and filter capabilities
- Card-based layouts
- Status badges
- Action buttons
- Responsive grids
- Loading states
- Empty states

## 🎨 UI Components Library

### Buttons
- `btn-primary` - Blue action button (#3B82F6)
- `btn-secondary` - Gray secondary button
- `btn-outline` - Purple outline button
- `btn-danger` - Red danger button
- `btn-add-property` - Purple gradient add button

### Badges
- `status-badge` - Status indicators (active, inactive, etc.)
- `occupancy-badge` - Occupancy levels (high, medium, low)
- `priority-badge` - Priority levels (high, medium, low)
- `role-badge` - User role display

### Cards
- `property-card` - Property display card
- `tenant-card` - Tenant information card
- `stat-card` - Statistics display card
- `info-card` - Information section card
- `settings-card` - Settings section card

## 📊 Data Models

### User
- id, username, email, password
- first_name, last_name
- role (ForeignKey to Role)
- phone, date_of_birth
- date_joined, last_login
- mfa_enabled

### Role
- id, name, description
- Permissions:
  - can_create_properties
  - can_edit_properties
  - can_delete_properties
  - can_manage_tenants
  - can_manage_leases
  - can_manage_financials
  - can_manage_users
  - can_view_analytics
  - can_export_reports

### Property
- id, name, type
- address, city, state, zip_code
- purchase_price, current_value
- total_units, occupied_units
- monthly_revenue, monthly_expenses
- owner (ForeignKey to Owner)

## 🔄 State Management (Pinia)

### Auth Store
```javascript
state: {
  user: null,
  token: null,
  refreshToken: null
}

actions: {
  login(credentials)
  register(userData)
  logout()
  refreshAccessToken()
  fetchUserDetails()
}

getters: {
  isAuthenticated
  userRole
  userPermissions
}
```

## 🛡️ Security Features

- JWT-based authentication
- Token refresh on expiration
- Password hashing (Django backend)
- Role-based access control
- Protected routes
- API request interceptors
- CORS configuration
- Input validation
- SQL injection prevention (Django ORM)

## 📱 Responsive Design

- Desktop-first approach
- Breakpoints:
  - Desktop: > 1024px
  - Tablet: 768px - 1024px
  - Mobile: < 768px
- Flexible grid layouts
- Touch-friendly buttons
- Mobile-optimized navigation

## 🎯 Future Enhancements

### Phase 1 (Immediate)
- [ ] Connect all API endpoints to real backend
- [ ] Implement file upload for profile photos
- [ ] Add real-time notifications
- [ ] Implement email verification
- [ ] Add password reset functionality

### Phase 2 (Short-term)
- [ ] Implement actual map integration (Google Maps/Mapbox)
- [ ] Add chart libraries (Chart.js/D3.js)
- [ ] Build document upload system
- [ ] Create mobile app (React Native)
- [ ] Add unit tests

### Phase 3 (Long-term)
- [ ] AI-powered insights implementation
- [ ] Automated lease reminders
- [ ] Payment integration (Stripe)
- [ ] Tenant portal
- [ ] Mobile app for maintenance requests

## 🐛 Known Issues & Limitations

1. **API Integration**: Most features use mock data, need backend implementation
2. **Charts**: Placeholder divs, need charting library integration
3. **Map**: Static placeholder, need Google Maps/Mapbox integration
4. **File Upload**: Not implemented yet
5. **Real-time Updates**: No WebSocket/polling for live data

## 📖 Developer Notes

### Code Style
- Vue 3 Composition API (setup script)
- ES6+ JavaScript
- Async/await for API calls
- Ref/reactive for state management
- Computed properties for derived state

### Best Practices
- Component-based architecture
- Separation of concerns
- DRY principle
- Consistent naming conventions
- Comprehensive error handling
- Loading states for async operations

### Testing Strategy
- Unit tests for components (TODO)
- Integration tests for API (TODO)
- E2E tests for critical flows (TODO)

## 🤝 Contributing Guidelines

1. Follow existing code style
2. Use meaningful commit messages
3. Test all changes thoroughly
4. Update documentation for new features
5. Create feature branches
6. Submit pull requests with descriptions

## 📄 License

Proprietary - All rights reserved

## 👨‍💻 Maintenance

### Regular Tasks
- Monitor error logs
- Update dependencies
- Backup database
- Review user feedback
- Optimize performance

### Version Control
- Use semantic versioning (MAJOR.MINOR.PATCH)
- Tag releases in Git
- Maintain changelog
- Document breaking changes

## 📞 Support

For issues or questions:
- Check documentation first
- Review existing issues
- Create detailed bug reports
- Include screenshots for UI issues

---

**Last Updated**: December 2024
**Version**: 1.0.0
**Status**: Active Development
