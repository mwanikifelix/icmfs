from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FinancialRecordViewSet, PaymentViewSet

router = DefaultRouter()
router.register(r"records", FinancialRecordViewSet, basename="finance-records")
router.register(r"payments", PaymentViewSet, basename="payments")

urlpatterns = [
    path("", include(router.urls)),
]
