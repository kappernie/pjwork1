from django.db import models
from users.models import Renter
from property.models import Property


class Payment(models.Model):
    STATUS = (('Accepted', 'Accepted'), ('Processing', 'Processing'),
              ('completed', 'completed'), ('Failed', 'Failed'))

    renter = models.ForeignKey(Renter, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    settled = models.BooleanField(default=False)
    duration = models.IntegerField(blank=True, null=True)
    settlement_date = models.DateTimeField(blank=True, null=True)
    currency = models.TextField(max_length=500, null=True)
    transaction_id = models.TextField(max_length=500, null=True)
    status = models.CharField(
        max_length=200, choices=STATUS, default='Processing', null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.renter.user.username} - GHS{self.amount} - {self.created_at}- {self.settled}"


class Plan(models.Model):
    # enums
    # status
    QUARTERLY = 1
    BIANUALLY = 2
    MONTHLY = 3

    INTERVALS = [
        (QUARTERLY, 'Quarterly'),
        (BIANUALLY, 'Bianually'),
        (MONTHLY, 'Monthly'),
    ]

    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    plan_code = models.CharField(max_length=512, null=True, blank=True)
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    down_payment_amt = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    total_amount_at_the_end_of_sub = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    onetime_payment_amt = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    interval = models.SmallIntegerField(choices=INTERVALS)
    invoice_limit = models.IntegerField(blank=True, null=True, default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.plan_code}'


class PaymentSubscription(models.Model):

    # enums
    # status
    ACTIVE = 1
    NON_RENEWING = 2
    ATTENTION = 3
    COMPLETED = 4
    CANCELLED = 5

    STATUSES = [
        (ACTIVE, 'Active'),
        (NON_RENEWING, 'Non renewing'),
        (ATTENTION, 'Attention'),
        (COMPLETED, 'Completed'),
        (CANCELLED, 'Cancelled'),
    ]

    down_payment = models.OneToOneField(
        Payment, on_delete=models.PROTECT)
    customer = models.ForeignKey(Renter, on_delete=models.PROTECT)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    status = models.SmallIntegerField(choices=STATUSES, default=ACTIVE)
    subscription_code = models.CharField(max_length=512, null=True, blank=True)
    email_token = models.CharField(max_length=512, null=True, blank=True)
    start_date = models.DateTimeField(blank=True, null=True)
    num_of_payments_made = models.SmallIntegerField(default=0)
    next_payment_date = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.subscription_code} - {self.plan.plan_code}'
