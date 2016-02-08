from django.db import models
from jamjar.base.models import BaseModel

class Artist(BaseModel):
    name = models.CharField(max_length=150)
    spotify_id = models.CharField(max_length=100, null=True)
    genres = models.ManyToManyField('artists.Genre',related_name='artists',blank=True)
    unofficial = models.BooleanField(default=False)

class Genre(BaseModel):
    name = models.CharField(max_length=100)