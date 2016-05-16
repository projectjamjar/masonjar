from django.db import models
from jamjar.base.models import BaseModel

from django.db.models.signals import pre_delete
from django.dispatch import receiver

from django.conf import settings

from datetime import datetime, timedelta
from math import log

from lilo import Lilo

import logging, uuid, os, shutil

import logging; logger = logging.getLogger(__name__)

# These are needed for the "hotness" score)
epoch = datetime(1970, 1, 1)
def epoch_seconds(date):
    td = date - epoch
    return td.days * 86400 + td.seconds + (float(td.microseconds) / 1000000)

class VideoQuerySet(models.query.QuerySet):
    def is_public(self):
        return self.filter(is_private=False)

    def is_uploaded(self):
        return self.filter(uploaded=True)

class PublicVideoManager(models.Manager):
    def get_queryset(self):
        return VideoQuerySet(self.model, using=self._db).is_public().is_uploaded()

    def for_user(self, user):
        excluded = user.blocks.filter(is_blocked=True).values_list('blocked_user_id', flat=True)
        return self.exclude(user_id__in=excluded)

class Video(BaseModel):

    user = models.ForeignKey('users.User', related_name='videos')
    name = models.CharField(max_length=128)
    uploaded = models.BooleanField(default=False)
    concert = models.ForeignKey('concerts.Concert', related_name='videos')
    uuid = models.UUIDField(default=uuid.uuid4,editable=False)
    length = models.FloatField(null=True)
    original_filename = models.CharField(max_length=256,null=True)
    file_size = models.FloatField(null=True)
    is_private = models.BooleanField(default=False)
    views = models.IntegerField(default=0)
    artists = models.ManyToManyField('artists.Artist', related_name='videos',blank=True)
    width  = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    recorded_at = models.DateTimeField(null=True)

    objects = PublicVideoManager()
    all_objects = models.Manager()

    class Meta:
        ordering = ['-created_at',]

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
        return self.make_s3_path('video','m3u8') if self.uploaded else None

    def web_src(self):
        return self.make_s3_path('video','mp4') if self.uploaded else None

    def thumb_src(self):
        if self.uploaded:
            thumbs = {}
            for size in settings.THUMBNAIL_SIZES:
                filename = 'thumb-{}'.format(size)
                thumbs[size] = self.make_s3_path(filename,'jpg')
            return thumbs
        else:
            return None

    def do_upload(self, input_fh):
        video_path = self.tmp_src()
        logger.info("Writing uploaded file to {:}".format(video_path))

        with open(video_path, 'wb+') as output_fh:
            # Split file into chunks to handle upload
            for chunk in input_fh.chunks():
                output_fh.write(chunk)

        # Check to make sure that this video hasn't been uploaded already
        lilo = Lilo(settings.LILO_CONFIG, video_path, self.id)
        already_fingerprinted = lilo.check_if_fingerprinted()

        if already_fingerprinted:
            logger.warn('Video re-upload attempted by user {} - Video id: {}'.format(self.user_id,self.id))
            raise Exception('This video has already been uploaded.')

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

    def hot(self, date):
        """
        Hotness score based on reddit's "hot" algorithm
        https://medium.com/hacking-and-gonzo/how-reddit-ranking-algorithms-work-ef111e33d0d9#.pphklly6z

        Start date is based on April 12, 2016, 2:26 EST
        """
        s = self.views
        order = log(max(abs(s), 1), 10)
        sign = 1 if s > 0 else -1 if s < 0 else 0
        seconds = epoch_seconds(date) - 1460427950
        return round(sign * order + seconds / 45000, 7)

"""
When deleting a video object, also delete the video files from the server
"""
@receiver(pre_delete, sender=Video)
def delete_file(sender, instance, **kwargs):
    # Delete the local file folder
    video_dir = instance.get_video_dir()
    if os.path.exists(video_dir):
        shutil.rmtree(video_dir)

    # TODO: Delete the file from S3 if it exists

    # TODO: Delete the fingerprints from lilo if there are any FOR THIS VIDEO ID

class PublicEdgeManager(models.Manager):
    def get_queryset(self):
        return super(PublicEdgeManager, self).get_queryset().filter(video1__is_private=False, video2__is_private=False)

class Edge(BaseModel):

    video1 = models.ForeignKey(Video, related_name='video1', db_index=True)
    video2 = models.ForeignKey(Video, related_name='video2', db_index=True)
    offset     = models.FloatField()
    confidence = models.IntegerField()

    objects = PublicEdgeManager()

    @classmethod
    def new(cls, video1_id, video2_id, offset, confidence):
        edge = Edge(video1_id=video1_id, video2_id=video2_id, offset=offset, confidence=confidence)
        edge.save()
        return edge

class JamJarMap(models.Model):
    video = models.ForeignKey(Video, related_name='jamjars')
    start = models.ForeignKey(Video, related_name='startjars')

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
    ('U','Report User'),
)

class VideoFlag(BaseModel):
    user = models.ForeignKey('users.User', related_name='flags_submitted')
    video = models.ForeignKey(Video, related_name='flags')
    flag_type = models.CharField(max_length=1, choices=FLAG_TYPES)
    notes = models.CharField(max_length=500,null=True,blank=True)

class JamPick(BaseModel):
    video = models.ForeignKey(Video, related_name='jampick')
