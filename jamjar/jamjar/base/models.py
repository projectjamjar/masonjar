from rest_framework.response import Response
from django.db import models

from django.http import HttpResponse
from wsgiref.util import FileWrapper

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


class VideoResponse(HttpResponse):

    "Constructor, takes path to video and returns a streaming url"
    def __init__(self, src):
        video_fh = FileWrapper(open(src, 'rb'))
        self['Content-Disposition'] = 'attachment; filename={:}'.format(src)

        super(VideoResponse, self).__init__(video_fh, content_type='video/mp4', status=200)

