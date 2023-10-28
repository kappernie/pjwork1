from django.db import models
from users.models import Lister


class PropertyType(models.Model):
    TYPE_CHOICES = (
        ('1B', '1 Bedroom'),
        ('2B', '2 Bedroom'),
        ('CA', 'Commercial Apartment'),
        ('MT', 'Mortgage Apartment'),
        ('4S', 'For Sale'),
        ('4R', 'For Rent'),
    )
    type = models.CharField(max_length=200, choices=TYPE_CHOICES)

    def get_type_display(self):
        for choice in self.TYPE_CHOICES:
            if choice[0] == self.type:
                return choice[1]

    def __str__(self):
        return f"{self.get_type_display()}"


class Location (models.Model):
    country = models.TextField(null=True, blank=True)
    Region = models.TextField(null=True, blank=True)
    city = models.TextField(null=True, blank=True)
    suburb = models.TextField(null=True, blank=True)
    code = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.country} - {self.Region}- {self.city} - {self.suburb}"


class Property(models.Model):

    CURRENCY_CHOICES = (
        ('USD', 'USD'),
        ('GHS', 'GHS'),
    )
    name = models.TextField(null=True, blank=True)
    location_text = models.CharField(max_length=200,  null=True, blank=True)
    property_types = models.ForeignKey(
        PropertyType, on_delete=models.CASCADE,  null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    lister = models.ForeignKey(Lister, null=True, on_delete=models.CASCADE)
    for_rent = models.BooleanField(default=False)
    # This is the duration in months. 12, 24, 36 etc.
    min_rent_duration = models.IntegerField(blank=True, null=True)
    max_rent_duration = models.IntegerField(blank=True, null=True)

    currency = models.CharField(
        max_length=200, choices=CURRENCY_CHOICES, null=True)
    description = models.TextField(max_length=10000, null=True, blank=True)
    Location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.Location}  -  {self.currency} {self.price}"

    class Meta:
        verbose_name_plural = 'properties'
        constraints = [
            models.CheckConstraint(
                check=(models.Q(for_rent=True) & models.Q(
                    min_rent_duration__isnull=False) & models.Q(
                    max_rent_duration__isnull=False)) | (models.Q(for_rent=False) & models.Q(min_rent_duration__isnull=True) & models.Q(
                        max_rent_duration__isnull=True)),
                name='rent_duration_required_if_for_rent'
            )
        ]


def get_property_images_upload_path(instance, filename):
    # Get the property id from the instance
    property_id = instance.property.id
    # Return the path with the property id and the filename
    return f"uploads/properties/{property_id}/{filename}"


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    upload = models.ImageField(upload_to=get_property_images_upload_path)

    def __str__(self):
        return f"{self.property}"
