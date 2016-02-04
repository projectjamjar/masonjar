from django.db import models
from jamjar.base.models import BaseModel

from django.db.models.signals import pre_delete
from django.dispatch import receiver

from django.conf import settings

import logging, uuid, os

class Video(BaseModel):

    user = models.ForeignKey('users.User', related_name='videos')
    name = models.CharField(max_length=128)
    uploaded = models.BooleanField(default=False)
    concert = models.ForeignKey('concerts.Concert', related_name='concert')
    tmp_src = models.CharField(max_length=128)              # where it lives on disk before upload to s3
    web_src = models.URLField(max_length=128, default="")  # s3 path, for streaming to web
    hls_src = models.URLField(max_length=128, default="")  # s3 path, for streaming to ios
    thumb_src = models.URLField(max_length=128, default="")
    length = models.FloatField()
    file_size = models.FloatField()
    is_private = models.BooleanField(default=False)
    views = models.IntegerField()
    artists = models.ManyToManyField('artists.Artist', related_name='videos')

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

        with open(video_filepath, 'wb+') as output_fh:
            # read 4k until an empty string is found
            for chunk in input_fh.chunks():
                output_fh.write(chunk)

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
        thumb_src = self.make_s3_path(video_uid, 'jpg')

        return {
            'tmp_src' : tmp_src,
            'hls_src' : hls_src,
            'web_src' : web_src,
            'thumb_src': thumb_src,
            'video_dir' : video_dir
        }

"""
When deleting a video object, also delete the video files from the server
"""
@receiver(pre_delete, sender=Video)
def delete_file(sender, instance, **kwargs):
    # Delete the file itself
    os.remove(instance.get_video_dir())

class Edge(BaseModel):

    video1 = models.ForeignKey(Video, related_name='video1', db_index=True)
    video2 = models.ForeignKey(Video, related_name='video2', db_index=True)
    offset     = models.FloatField()
    confidence = models.IntegerField()

    @classmethod
    def new(cls, video1_id, video2_id, offset, confidence):
        edge = Edge(video1_id=video1_id, video2_id=video2_id, offset=offset, confidence=confidence)
        edge.save()
        return edge

class Playlist(BaseModel):
    user = models.ForeignKey('users.User',related_name='playlists')
    name = models.CharField(max_length=100)
    is_private = models.BooleanField(default=False)
    videos = models.ManyToManyField(Video, related_name='playlists',through='PlaylistOrder')

class PlaylistOrder(models.Model):
    number = models.PositiveIntegerField()
    playlist = models.ForeignKey(Playlist)
    video = models.ForeignKey(Video)

    class Meta:
        ordering = ('number',)

class VideoVote(BaseModel):
    user = models.ForeignKey('users.User',related_name='votes')
    video = models.ForeignKey(Video, related_name='votes')
    vote = models.NullBooleanField(null=True) # True is upvote, False is downvote, null is blank (redacted vote)

FLAG_TYPES = (
    ('Q','Quality'),
    ('I','Inappropriate'),
    ('A','Accuracy'),
)

class VideoFlag(BaseModel):
    user = models.ForeignKey('users.User', related_name='flags_submitted')
    video = models.ForeignKey(Video, related_name='flags')
    flag_type = models.CharField(max_length=1, choices=FLAG_TYPES)
    notes = models.CharField(max_length=500,null=True,blank=True)
