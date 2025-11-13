# Smart Real Estate Portfolio Management System

A comprehensive web-based platform for property investment firms with Django backend and Vue.js frontend.

## Project Structure

```
smart-property-manager/
├── backend/          # Django REST API
├── frontend/         # Vue.js Application
└── README.md
```

## Tech Stack

### Backend
- Django 4.2+ with Django REST Framework
- PostgreSQL with PostGIS
- JWT Authentication with MFA
- AWS S3 for document storage
- Redis for caching

### Frontend
- Vue 3 with Vite
- Pinia for state management
- Vue Router
- Chart.js for analytics
- Google Maps API
- Axios for API calls

## Getting Started

### Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## Features

- ✅ Role-Based Access Control (RBAC)
- ✅ Multi-Factor Authentication (MFA)
- ✅ Property Portfolio Management
- ✅ Tenant CRM
- ✅ Lease Management
- ✅ Financial Tracking
- ✅ Maintenance Management
- ✅ Geospatial Property Mapping
- ✅ AI-Powered Insights
- ✅ Document Management with AWS S3
- ✅ Analytics & Reporting

## Design

UI/UX strictly follows the Figma design file: `Smart Property Manager.fig`
