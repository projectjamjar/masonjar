from django.db import models
from jamjar.base.models import BaseModel

class Artist(BaseModel):
    name = models.CharField(max_length=150)
    musicgraph_id = models.CharField(max_length=100, null=True)
    unofficial = models.BooleanField(default=False)
    # created_by = models.ForeignKey('users.User',related_name='added_artists')
