from django.db import models
from django.db.models import Q
from jamjar.base.models import BaseModel
import operator

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

    @classmethod
    def search_venues(cls, search_string):
        q_list = []

        # For each word in the search string, filter things
        for word in search_string.split():
            q_list.append( Q(name__icontains=word) )
            q_list.append( Q(city__icontains=word) )

        query = reduce(operator.or_,q_list)

        venues = cls.objects.filter(query)

        return venues
