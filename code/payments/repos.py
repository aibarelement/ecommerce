import logging
import uuid
from typing import Protocol

from django.db import transaction
from rest_framework.generics import get_object_or_404

from payments import models, choices


logger = logging.getLogger(__name__)


class BillReposInterface(Protocol):

    @staticmethod
    def pay_bill(bill_id: uuid.UUID) -> None: ...


class BillReposV1:

    @staticmethod
    def pay_bill(bill_id: uuid.UUID) -> None:
        with transaction.atomic():
            try:
                bill = get_object_or_404(
                    models.Bill.objects.filter(
                        id=bill_id,
                        status=choices.BillStatusChoices.New,
                    ),
                )
                bill.status = choices.BillStatusChoices.Paid
                bill.save()

                models.Transaction.objects.create(
                    bill=bill,
                    amount_currency=bill.amount_currency,
                    amount=bill.amount,
                    transaction_type=choices.TransactionTypeChoices.Ok,
                )
            except models.Bill.DoesNotExist:
                logger.error(f'bill with id {bill_id} not found')
            finally:
                logger.info(f'bill with id {bill_id} is successfully paid!')
