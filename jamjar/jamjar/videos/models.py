from django.db import models
from jamjar.base.models import BaseModel

class Video(BaseModel):
    name = models.CharField(max_length=128)
    src = models.CharField(max_length=128)