from django.db import models


class BillStatusChoices(models.TextChoices):
    New = 'New'
    Pending = 'Pending'
    Paid = 'Paid'
    Expired = 'Expired'
    Refund = 'Refund'
    RefundPartially = 'RefundPartially'


class TransactionTypeChoices(models.TextChoices):
    Ok = 'Ok'
    Refund = 'Refund'
