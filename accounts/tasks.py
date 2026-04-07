from celery import shared_task
from .services import IllustrationService
from .models import Calculation, User


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