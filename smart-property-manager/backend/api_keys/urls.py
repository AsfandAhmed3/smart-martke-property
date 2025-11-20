from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import APIKeyViewSet, APIKeyUsageLogViewSet

router = DefaultRouter()
router.register(r'keys', APIKeyViewSet, basename='api-key')
router.register(r'usage-logs', APIKeyUsageLogViewSet, basename='api-key-usage-log')

urlpatterns = [
    path('', include(router.urls)),
]
