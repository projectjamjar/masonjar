from rest_framework.response import Response
from django.db import models

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class SuccessResponse(Response):

    "Constructor, takes data and puts in the correct field"
    def __init__(self, data):
        data = data
        super(SuccessResponse, self).__init__(data, status=200)

class ErrorResponse(Response):

    "Constructor, takes data and puts in the correct field"
    def __init__(self, error, status):
        data = {
            "error": error
        }
        super(ErrorResponse, self).__init__(data, status=status)