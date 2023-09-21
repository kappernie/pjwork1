from django.db import models

# Create your models here.

class settled(models.Model):

    is_settled = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.is_settled}"