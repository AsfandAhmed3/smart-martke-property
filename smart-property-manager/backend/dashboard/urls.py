from django.urls import path
from .views import DashboardStatisticsView, PropertyPerformanceView

urlpatterns = [
    path('statistics/', DashboardStatisticsView.as_view(), name='dashboard-statistics'),
    path('stats/', DashboardStatisticsView.as_view(), name='dashboard-stats-alias'),
    path('property-performance/', PropertyPerformanceView.as_view(), name='property-performance'),
]
