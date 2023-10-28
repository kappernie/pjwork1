from django.db import models
from django.contrib.auth.models import User


# class Agent(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     verified = models.BooleanField(default=False)

#     def __str__(self):
#         return self.user.username

# add a model called Lister, same attrs as Realtor but with an additional attribute of classificatio (enum agent, owner)

# Implement agent-owner-renter sign up and sign in
# See if I can have an agent/owner submit request for adding a listing
# Admin approve interface
# Owner/agent can mark a listing as sold
# There are the property owners themselves or licensed real estate agents acting on behalf of property owners


class Lister(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    onboarding_completed = models.BooleanField(default=False)
    phone = models.CharField(max_length=1000, null=True, blank=True)
    Bank_details = models.TextField(null=True, blank=True)
    business_document = models.FileField(
        upload_to='uploads/documents',  null=True, blank=True)
    classification = models.CharField(max_length=1000, null=True, choices=[
        ('owner', 'Owner'),
        ('agent', 'Agent'),
    ])

    def __str__(self):
        return self.user.username


class Renter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    verified = models.BooleanField(default=False)
    phone = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.user.username
