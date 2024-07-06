import time
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

    response = api_client.post('/api/rentals/rent/', {'bicycle_id': test_bicycle.id})

    assert response.status_code == 201
    assert Rental.objects.count() == initial_rental_count + 1
    assert not Bicycle.objects.get(id=test_bicycle.id).is_available


@pytest.mark.django_db
def test_get_rental_history(api_client, test_user, test_bicycle, test_rental_id):
    api_client.force_authenticate(user=test_user)
    initial_rental_count = Rental.objects.count()
    Rental.objects.create(user=test_user, bicycle=test_bicycle)

    response = api_client.get('/api/rentals/history/')

    assert response.status_code == 200
    assert len(response.data) == initial_rental_count + 1


@pytest.mark.django_db
def test_rental_calculation(api_client, test_user, test_bicycle):
    rental = Rental.objects.create(
        user=test_user,
        bicycle=test_bicycle,
        start_time=timezone.now(),
        end_time=timezone.now() + timezone.timedelta(hours=1),
    )

    task_result = calculate_rental_cost.delay(rental.id)

    assert task_result is not None


