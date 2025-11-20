from rest_framework import status, generics, views
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import Role
from .serializers import (
    UserSerializer,
    RegisterSerializer,
    LoginSerializer,
    ChangePasswordSerializer,
    RoleSerializer,
    UpdateProfileSerializer,
    NotificationPreferencesSerializer,
    AdminUserManagementSerializer,
    CreateUserSerializer
)

User = get_user_model()


class IsSuperAdmin(IsAuthenticated):
    """Permission class for superadmin only access"""
    def has_permission(self, request, view):
        return super().has_permission(request, view) and (
            request.user.is_superadmin or request.user.is_superuser
        )


class RegisterView(generics.CreateAPIView):
    """User registration endpoint"""
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)


class LoginView(views.APIView):
    """User login endpoint"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        })


class LogoutView(views.APIView):
    """User logout endpoint"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
        except Exception:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """Get and update user profile"""
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    
    def get_object(self):
        return self.request.user


class ChangePasswordView(views.APIView):
    """Change user password"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        
        # Check old password
        if not user.check_password(serializer.validated_data['old_password']):
            return Response(
                {'error': 'Old password is incorrect'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Set new password
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        return Response({'message': 'Password changed successfully'})


class RoleListView(generics.ListAPIView):
    """List all available roles"""
    queryset = Role.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = RoleSerializer


class UpdateProfileView(views.APIView):
    """Update user profile information"""
    permission_classes = [IsAuthenticated]
    
    def put(self, request):
        serializer = UpdateProfileSerializer(
            instance=request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({
            'message': 'Profile updated successfully',
            'user': UserSerializer(request.user).data
        })


class NotificationPreferencesView(views.APIView):
    """Get and update notification preferences"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        serializer = NotificationPreferencesSerializer(request.user)
        return Response(serializer.data)
    
    def put(self, request):
        serializer = NotificationPreferencesSerializer(
            instance=request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({
            'message': 'Notification preferences updated successfully',
            'preferences': serializer.data
        })


class ToggleMFAView(views.APIView):
    """Enable or disable two-factor authentication"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = request.user
        enable = request.data.get('enable', False)
        
        user.mfa_enabled = enable
        user.save()
        
        return Response({
            'message': f'Two-factor authentication {"enabled" if enable else "disabled"} successfully',
            'mfa_enabled': user.mfa_enabled
        })


# ===== SUPERADMIN VIEWS =====

class AdminUserListView(generics.ListAPIView):
    """List all users (superadmin only)"""
    permission_classes = [IsSuperAdmin]
    serializer_class = AdminUserManagementSerializer
    
    def get_queryset(self):
        queryset = User.objects.select_related('role').all()
        
        # Filter by search query
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(email__icontains=search) |
                Q(username__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search)
            )
        
        # Filter by role
        role_id = self.request.query_params.get('role', None)
        if role_id:
            queryset = queryset.filter(role_id=role_id)
        
        # Filter by active status
        is_active = self.request.query_params.get('is_active', None)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        # Filter by superadmin status
        is_superadmin = self.request.query_params.get('is_superadmin', None)
        if is_superadmin is not None:
            queryset = queryset.filter(is_superadmin=is_superadmin.lower() == 'true')
        
        return queryset.order_by('-created_at')


class AdminUserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Get, update, or delete a specific user (superadmin only)"""
    permission_classes = [IsSuperAdmin]
    serializer_class = AdminUserManagementSerializer
    queryset = User.objects.select_related('role').all()
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class AdminCreateUserView(generics.CreateAPIView):
    """Create a new user (superadmin only)"""
    permission_classes = [IsSuperAdmin]
    serializer_class = CreateUserSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        return Response({
            'message': 'User created successfully',
            'user': AdminUserManagementSerializer(user).data
        }, status=status.HTTP_201_CREATED)


class AdminToggleSuperadminView(views.APIView):
    """Promote or demote a user to/from superadmin (superadmin only)"""
    permission_classes = [IsSuperAdmin]
    
    def post(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Toggle superadmin status
        user.is_superadmin = not user.is_superadmin
        user.save()
        
        return Response({
            'message': f'User {"promoted to" if user.is_superadmin else "demoted from"} superadmin successfully',
            'user': AdminUserManagementSerializer(user).data
        })


class AdminUserStatsView(views.APIView):
    """Get user statistics (superadmin only)"""
    permission_classes = [IsSuperAdmin]
    
    def get(self, request):
        total_users = User.objects.count()
        active_users = User.objects.filter(is_active=True).count()
        superadmins = User.objects.filter(is_superadmin=True).count()
        
        # Users by role
        users_by_role = {}
        for role in Role.objects.all():
            users_by_role[role.name] = User.objects.filter(role=role).count()
        
        return Response({
            'total_users': total_users,
            'active_users': active_users,
            'inactive_users': total_users - active_users,
            'superadmins': superadmins,
            'users_by_role': users_by_role
        })
