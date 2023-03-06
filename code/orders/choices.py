from django.db import models


class OrderStatusChoices(models.TextChoices):
    New = 'New'
    ProcessInProgress = 'ProcessInProgress'
    Cancel = 'Cancel'
    Paid = 'Paid'
