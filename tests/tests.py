import time
from unittest.mock import MagicMock, patch
from django.utils import timezone
import pytest
from core.tasks import calculate_rental_cost
from core.models import Rental, Bicycle


@pytest.fixture(scope='session')
def celery_config():
    return {
        'broker_url': 'memory://',
        'result_backend': 'django-db',
        'task_always_eager': True,
        'task_eager_propagates': True,
    }


@pytest.mark.django_db
def test_rent_bicycle(api_client, test_user, test_bicycle):
    api_client.force_authenticate(user=test_user)
    initial_rental_count = Rental.objects.count()

    response = api_client.post(
        '/api/rentals/rent/', {'bicycle_id': test_bicycle.id})

    assert response.status_code == 201
    assert Rental.objects.count() == initial_rental_count + 1
    assert not Bicycle.objects.get(id=test_bicycle.id).is_available


@pytest.mark.django_db
def test_get_rental_history(api_client, test_user, test_bicycle):
    api_client.force_authenticate(user=test_user)
    initial_rental_count = Rental.objects.count()
    Rental.objects.create(user=test_user, bicycle=test_bicycle)

    response = api_client.get('/api/rentals/history/')

    assert response.status_code == 200
    assert len(response.data) == initial_rental_count + 1


@pytest.mark.django_db
def test_calculate_rental_cost_success():
    # Mocking the Rental model and its methodsA
    rental = MagicMock(spec=Rental)
    rental.start_time = MagicMock()
    rental.end_time = MagicMock()
    rental.start_time = timezone.now()
    rental.end_time = timezone.now() + timezone.timedelta(hours=1)
    rental.id = 1

    with patch('core.models.Rental.objects.get', return_value=rental):
        calculate_rental_cost(rental.id)

        rental.save.assert_called_once()
        assert rental.cost == 100

