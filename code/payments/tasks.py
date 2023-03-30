import logging
import uuid

from src.celery import app

from payments import models, choices


logger = logging.getLogger(__name__)


@app.task()
def check_bill_expires_at(bill_id: uuid.UUID) -> None:
    try:
        bill = models.Bill.objects.filter(
            pk=bill_id,
            status=choices.BillStatusChoices.New,
        )
        bill.status = choices.BillStatusChoices.Expired
        bill.save()
        logger.info(f'Bill with id {bill_id} set status "EXPIRED"')
    except models.Bill.DoesNotExist as e:
        logger.error(f'Bill with id {bill_id} not found')

