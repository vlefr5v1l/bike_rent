from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.utils import timezone
from core.models import Bicycle, Rental
from .serializers import UserSerializer, BicycleSerializer, RentalSerializer
from core.tasks import calculate_rental_cost
import time


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class BicycleViewSet(viewsets.ModelViewSet):
    queryset = Bicycle.objects.all()
    serializer_class = BicycleSerializer

    @action(detail=False, methods=['get'])
    def available(self, request):
        available_bicycles = Bicycle.objects.filter(is_available=True)
        serializer = self.get_serializer(available_bicycles, many=True)
        return Response(serializer.data)


class RentalViewSet(viewsets.ModelViewSet):
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def rent(self, request):
        user = request.user
        bicycle_id = request.data.get('bicycle_id')

        if Rental.objects.filter(user=user, end_time__isnull=True).exists():
            return Response({"error": "You already have an active rental"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            bicycle = Bicycle.objects.get(id=bicycle_id, is_available=True)
        except Bicycle.DoesNotExist:
            return Response({"error": "Bicycle not available"}, status=status.HTTP_400_BAD_REQUEST)

        rental = Rental.objects.create(user=user, bicycle=bicycle)
        bicycle.is_available = False
        bicycle.save()

        return Response(RentalSerializer(rental).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def return_bicycle(self, request, pk=None):
        rental = self.get_object()
        if rental.end_time:
            return Response({"error": "This rental has already ended"}, status=status.HTTP_400_BAD_REQUEST)

        rental.end_time = timezone.now()
        rental.save()

        rental.bicycle.is_available = True
        rental.bicycle.save()

        calculate_rental_cost.delay(rental.id)
        time.sleep(1)

        rental.refresh_from_db()

        return Response(RentalSerializer(rental).data)

    @action(detail=False, methods=['get'])
    def history(self, request):
        user_rentals = Rental.objects.filter(user=request.user)
        serializer = RentalSerializer(user_rentals, many=True)
        return Response(serializer.data)
