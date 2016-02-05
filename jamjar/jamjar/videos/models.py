from django.db import models
from jamjar.base.models import BaseModel

from django.db.models.signals import pre_delete
from django.dispatch import receiver

from django.conf import settings

import logging, uuid, os

import logging; logger = logging.getLogger(__name__)

class Video(BaseModel):

    user = models.ForeignKey('users.User', related_name='videos')
    name = models.CharField(max_length=128)
    uploaded = models.BooleanField(default=False)
    concert = models.ForeignKey('concerts.Concert', related_name='concert')
    uuid = models.UUIDField(default=uuid.uuid4,editable=False)
    length = models.FloatField(null=True)
    original_filename = models.CharField(max_length=256,null=True)
    file_size = models.FloatField(null=True)
    is_private = models.BooleanField(default=False)
    views = models.IntegerField(default=0)
    artists = models.ManyToManyField('artists.Artist', related_name='videos')

    def get_video_dir(self):
        " Get the local directory for the video (and other temp files) "
        return '{:}/{:}'.format(settings.TMP_VIDEOS_PATH, self.uuid)

    def get_video_filepath(self, extension, filename="video"):
        " Get the local filepath for a file related to this video "
        full_filename = '{:}.{:}'.format(filename, extension)
        return os.path.join(self.get_video_dir(), full_filename)

    def tmp_src(self):
        return os.path.join(self.get_video_dir(), self.original_filename)

    def hls_src(self):
        return self.make_s3_path('video','m3u8')

    def web_src(self):
        return self.make_s3_path('video','mp4')

    def thumb_src(self):
        return self.make_s3_path('thumb','jpg')

    def do_upload(self, input_fh):
        video_path = self.tmp_src()
        logger.info("Writing uploaded file to {:}".format(video_path))

        with open(video_path, 'wb+') as output_fh:
            # Split file into chunks to handle upload
            for chunk in input_fh.chunks():
                output_fh.write(chunk)

        return video_path

    def make_s3_path(self, filename, extension):
        return settings.S3_URL.format(self.uuid, filename, extension)

    def process_upload(self, input_fh):
        """
        Get the local directory where the video will temporarily live until
        uploaded to S3 and create it if it doesn't exist (it shouldn't)
        """
        video_dir = self.get_video_dir()
        if not os.path.exists(video_dir): os.makedirs(video_dir)

        return self.do_upload(input_fh)

"""
When deleting a video object, also delete the video files from the server
"""
@receiver(pre_delete, sender=Video)
def delete_file(sender, instance, **kwargs):
    # Delete the local file folder
    video_dir = instance.get_video_dir()
    if os.path.exists(video_dir):
        os.remove(video_dir)

    # TODO: Delete the file from S3 if it exists

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
