from django.db import models
from jamjar.base.models import BaseModel

class Video(BaseModel):
    name = models.CharField(max_length=128)

    # where it lives on disk before upload to s3
    tmp_src = models.CharField(max_length=128)

    # s3 path, for streaming to web
    web_src = models.CharField(max_length=128)

    # s3 path, for streaming to ios
    hls_src = models.CharField(max_length=128)

