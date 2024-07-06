from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, BicycleViewSet, RentalViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'bicycles', BicycleViewSet)
router.register(r'rentals', RentalViewSet)

urlpatterns = [
    path('', include(router.urls)),
]