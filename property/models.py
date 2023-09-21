from django.db import models
from users.models import Realtor


class PropertyType(models.Model): 
    TYPE_CHOICES = (
            ('1B', '1 Bedroom'),
            ('2B', '2 Bedroom'),
            ('CA', 'Commercial Apartment'),
            ('MT', 'Mortgage Apartment'),
            ('4S', 'For Sale'),
            ('4R', 'For Rent'),
        )
    type = models.CharField(max_length=200 , choices=TYPE_CHOICES)

    def __str__(self):
        return f"{self.type}"

class Location (models.Model):
    country = models.TextField( null=True , blank=True)
    Region = models.TextField( null=True , blank=True)
    city = models.TextField( null=True , blank=True)
    suburb = models.TextField( null=True , blank=True)
    code = models.TextField( null=True , blank=True)

    def __str__(self):
        return f"{self.country} - {self.Region}- {self.city} - {self.suburb}"

class Property(models.Model):
 
    CURRENCY_CHOICES = (
        ('$', '$'),
        ('GHS', 'GHS'),
    )
    name = models.TextField(null=True , blank = True)
    location_text = models.CharField(max_length=200 ,  null=True , blank=True)
    property_types = models.ForeignKey(PropertyType , on_delete=models.CASCADE ,  null=True , blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    realtor = models.ForeignKey(Realtor, on_delete=models.CASCADE)
    currency = models.CharField(max_length=200,choices= CURRENCY_CHOICES , null=True)
    description = models.TextField(max_length=10000 , null=True , blank=True)
    Location = models.ForeignKey(Location,on_delete=models.CASCADE , null=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return  f"{self.name} - {self.Location}  -  {self.currency} {self.price}"
    
class PropertyImage(models.Model): 
    property = models.ForeignKey(Property,on_delete=models.CASCADE)
    upload = models.ImageField(upload_to ='uploads/')

    def __str__(self):
        return f"{self.property}"
  
   



 