import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from core.models import Bicycle, Rental

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def test_user(db):
    user = User.objects.create_user(username='testuser', password='testpass')
    yield user
    user.delete()

@pytest.fixture
def test_bicycle(db):
    bicycle = Bicycle.objects.create(name='Test Bike')
    yield bicycle
    bicycle.delete()

@pytest.fixture
def test_rental_id(db):
    rental_id = Rental.objects.create(name='Test Bike')
    yield bicycle
    bicycle.delete()