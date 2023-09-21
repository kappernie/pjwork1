from django.db import models
from users.models import Renter
from property.models import Property

class Payment(models.Model):
    STATUS = (('Accepted', 'Accepted'),('Processing', 'Processing'),('completed', 'completed'),('Failed', 'Failed'))

    renter = models.ForeignKey(Renter, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    settled = models.BooleanField(default=False)
    settlement_date = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)
    currency = models.TextField(max_length= 500 , null=True)
    transaction_id = models.TextField(max_length= 500 , null=True)
    status = models.CharField(max_length=200,choices= STATUS , null=True)


    def __str__(self):
        return f"{self.renter.user.username} - ${self.amount} - {self.created}- {self.settled}"
