from django.db import models
from jamjar.base.models import BaseModel

class Concert(BaseModel):
    date = models.DateField()
    venue = models.ForeignKey('venues.Venue',related_name='concerts')
