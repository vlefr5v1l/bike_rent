from celery import shared_task
from .models import Rental

@shared_task
def calculate_rental_cost(rental_id):
    try:
        rental = Rental.objects.get(id=rental_id)
        duration = (rental.end_time - rental.start_time).total_seconds() / 3600
        cost_per_hour = 100
        cost = duration * cost_per_hour
        rental.cost = cost
        rental.save()
        print(f"Calculated cost: {cost}")
        return cost
    except Rental.DoesNotExist:
        print("Rental not found")