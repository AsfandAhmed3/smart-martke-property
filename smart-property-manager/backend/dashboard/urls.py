from django.urls import path
from .views import DashboardStatisticsView, PropertyPerformanceView

urlpatterns = [
    path('stats/', DashboardStatisticsView.as_view(), name='dashboard-statistics'),
    path('property-performance/', PropertyPerformanceView.as_view(), name='property-performance'),
]
