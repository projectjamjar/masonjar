from django.db import models
from jamjar.base.models import BaseModel

from django.conf import settings

import logging, uuid, os

class Video(BaseModel):

    name = models.CharField(max_length=128)
    tmp_src = models.CharField(max_length=128)              # where it lives on disk before upload to s3
    web_src = models.CharField(max_length=128, default="")  # s3 path, for streaming to web
    hls_src = models.CharField(max_length=128, default="")  # s3 path, for streaming to ios
    uploaded = models.BooleanField(default=False)

    @classmethod
    def get_video_dir(self, uuid):
        return '{:}/{:}'.format(settings.VIDEOS_PATH, uuid)

    @classmethod
    def get_video_filepath(self, video_dir, extension, filename="video"):
        full_filename = '{:}.{:}'.format(filename, extension)
        return os.path.join(video_dir, full_filename)


    @classmethod
    def do_upload(self, input_fh, video_filepath):
        logger = logging.getLogger(__name__)

        logger.info("Writing uploaded file to {:}".format(video_filepath))

        with open(video_filepath, 'wb') as output_fh:
            output_fh.write(input_fh.read())

        return video_filepath

    @classmethod
    def make_s3_path(self, uuid, extension):
      return 'https://s3.amazonaws.com/jamjar-videos/{:}/{:}/video.{:}'.format(settings.JAMJAR_ENV, uuid, extension)

    @classmethod
    def process_upload(self, input_fh):
        video_uid = uuid.uuid4()

        video_dir  = self.get_video_dir(video_uid)

        if not os.path.exists(video_dir): os.makedirs(video_dir)

        video_filepath = self.get_video_filepath(video_dir, 'mp4')

        tmp_src = self.do_upload(input_fh, video_filepath)
        hls_src = self.make_s3_path(video_uid, 'm3u8')
        web_src = self.make_s3_path(video_uid, 'mp4')

        return {
            'tmp_src' : tmp_src,
            'hls_src' : hls_src,
            'web_src' : web_src,
            'video_dir' : video_dir
        }


class Edge(BaseModel):

    video1 = models.ForeignKey(Video, related_name='video1')
    video2 = models.ForeignKey(Video, related_name='video2')
    offset     = models.FloatField()
    confidence = models.IntegerField()

    @classmethod
    def new(cls, video1_id, video2_id, offset, confidence):
        edge = Edge(video1_id=video1_id, video2_id=video2_id, offset=offset, confidence=confidence)
        edge.save()
        return edge
