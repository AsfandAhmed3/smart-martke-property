from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RevenueViewSet,
    ExpenseViewSet,
    TransactionViewSet,
    PaymentViewSet,
    AnalyticsView,
    PropertyPerformanceView,
    MonthlyRevenueView
)

app_name = 'financials'

router = DefaultRouter()
router.register(r'revenues', RevenueViewSet, basename='revenue')
router.register(r'expenses', ExpenseViewSet, basename='expense')
router.register(r'transactions', TransactionViewSet, basename='transaction')
router.register(r'payments', PaymentViewSet, basename='payment')

urlpatterns = [
    path('', include(router.urls)),
    path('analytics/', AnalyticsView.as_view(), name='analytics'),
    path('analytics/property-performance/', PropertyPerformanceView.as_view(), name='property_performance'),
    path('analytics/monthly-revenue/', MonthlyRevenueView.as_view(), name='monthly_revenue'),
]
