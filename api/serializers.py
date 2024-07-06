from rest_framework import serializers
from django.contrib.auth.models import User
from core.models import Bicycle, Rental

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class BicycleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bicycle
        fields = '__all__'

class RentalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields = '__all__'
        read_only_fields = ['is_available']