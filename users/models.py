from django.db import models
from django.contrib.auth.models import User

class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class Realtor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    onboarding_completed = models.BooleanField(default=False)
    Bank_details = models.TextField( null=True , blank=True)
    business_document = models.FilePathField(path = 'media/uploads/documents' ,  null=True , blank=True)

    def __str__(self):
        return self.user.username

class Renter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    verified = models.BooleanField(default=False)


    def __str__(self):
        return self.user.username


