from django.db import models
from jamjar.base.models import BaseModel

class Venue(BaseModel):
    name = models.CharField(max_length=100)
    place_id = models.CharField(max_length=100, null=True, blank=True)
    unofficial = models.BooleanField(default=False) # If this place is non-google-mappable (e.g: "Bob's Basement")
    formatted_address = models.CharField(max_length=1000, null=True, blank=True)
    lat = models.DecimalField(max_digits=12,decimal_places=8,null=True)
    lng = models.DecimalField(max_digits=12,decimal_places=8,null=True)
    utc_offset = models.IntegerField(null=True)
    website = models.URLField(null=True)
    city = models.CharField(max_length=50,null=True,blank=True)
    state = models.CharField(max_length=50,null=True,blank=True)
    state_short = models.CharField(max_length=10,null=True,blank=True)
    country = models.CharField(max_length=50,null=True,blank=True)
    country_short = models.CharField(max_length=10,null=True,blank=True)
