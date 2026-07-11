from celery import shared_task
from .services import IllustrationService
from .models import Calculation, User


'''
This code defines a Celery background task that:

Runs heavy calculation logic asynchronously
Saves input/output into the database
Returns the result without blocking the main API


🔄 Working Flow
API receives request → sends data to Celery task
Celery worker executes run_calculation in background
Business logic runs via IllustrationService
Result is stored in Calculation table
Task returns response (id + result)

Use Celery for long-running tasks
Keep business logic in service layer (clean architecture)
Store request/response for tracking history

'''


@shared_task
def run_calculation(data):

    # 🔥 Run business logic
    result = IllustrationService().execute(data)

    user = User.objects.first()

    # Convert dob to string
    data["dob"] = str(data["dob"])

    calc = Calculation.objects.create(
        user=user,
        input_data=data,
        output_data=result
    )

    return {
        "id": calc.id,
        "output": result
    }