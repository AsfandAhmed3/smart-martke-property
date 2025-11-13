from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView,
    LoginView,
    LogoutView,
    UserProfileView,
    ChangePasswordView,
    RoleListView,
    UpdateProfileView,
    NotificationPreferencesView,
    ToggleMFAView
)

app_name = 'users'

urlpatterns = [
    # Authentication
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # User Profile
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile/update/', UpdateProfileView.as_view(), name='update_profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('notification-preferences/', NotificationPreferencesView.as_view(), name='notification_preferences'),
    path('toggle-mfa/', ToggleMFAView.as_view(), name='toggle_mfa'),
    
    # Roles
    path('roles/', RoleListView.as_view(), name='roles'),
]
