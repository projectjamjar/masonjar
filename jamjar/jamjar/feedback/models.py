from django.db import models
from jamjar.base.models import BaseModel

class Feedback(BaseModel):
    email = models.EmailField()
    name = models.CharField(max_length=100)
    relevant_url = models.CharField(max_length=500, null=True, blank=True)
    feedback = models.CharField(max_length=2500)
