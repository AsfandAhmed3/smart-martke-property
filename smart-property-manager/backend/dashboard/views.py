from rest_framework.views import APIView  # type: ignore[import]
from rest_framework.response import Response  # type: ignore[import]
from rest_framework.permissions import IsAuthenticated  # type: ignore[import]
from django.utils import timezone  # type: ignore[import]


class DashboardStatisticsView(APIView):
    """Simplified dashboard statistics endpoint."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        stats = {
            'user': {
                'username': user.username,
                'email': user.email,
                'full_name': f"{user.first_name} {user.last_name}".strip() or user.username,
            },
            'welcome_message': f'Welcome back, {user.first_name or user.username}!',
            'current_time': timezone.now().isoformat(),
        }
        return Response(stats)


class PropertyPerformanceView(APIView):
    """Placeholder property performance endpoint."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'properties': [], 'total_properties': 0})
