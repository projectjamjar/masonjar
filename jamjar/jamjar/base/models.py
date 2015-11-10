from rest_framework.response import Response
from django.db import models

from django.http import HttpResponse

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

        path = '/opt/code/masonjar/videos/' + src
        print "Getting: ", path
        with open(path, 'rb') as fh:
            super(VideoResponse, self).__init__(fh, content_type='application/vnd.apple.mpegurl', status=200)

        # ffmpeg -i in.mp4 out.m3u8

