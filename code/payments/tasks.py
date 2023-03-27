import uuid

from src.celery import app

from payments import models, choices


@app.task()
def check_bill_expires_at(bill_id: uuid.UUID) -> None:
    models.Bill.objects.filter(
        pk=bill_id,
        status=choices.BillStatusChoices.New,
    ).update(
        status=choices.BillStatusChoices.Expired,
    )
