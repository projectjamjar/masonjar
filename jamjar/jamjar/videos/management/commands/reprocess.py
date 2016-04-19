from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from jamjar.tasks.transcode_video import VideoTranscoder
from jamjar.videos.models import Video

import boto3, botocore.exceptions
import os, sys

class Command(BaseCommand):
    help = 'Reprocess a uploaded video. Transcodes to HLS and re-uploads to S3'

    def add_arguments(self, parser):
        parser.add_argument('video_id', type=int)

    def download_source(self, video):
        filename = 'video.mp4'
        local_dir = video.get_video_dir()

        disk_path = os.path.join(local_dir, filename)
        s3_path = os.path.join(settings.JAMJAR_ENV, str(video.uuid), filename)

        if not os.path.exists(local_dir):
            os.makedirs(local_dir)

        print "Downloading {} to {}".format(s3_path, local_dir)

        self.s3.Object('jamjar-videos', s3_path).download_file(disk_path)

    def handle(self, *args, **options):
        self.s3 = boto3.resource('s3')
        video_id = options['video_id']

        transcoder = VideoTranscoder()
        video = Video.objects.get(pk=video_id)

        transcoder.video = video # hack, sorry

        try:
            self.download_source(video)
        except botocore.exceptions.ClientError as e:
            print "The video with id {} wasn't found in S3!".format(video.id)
            sys.exit(1)

        if not transcoder.transcode_to_hls():
            print "Error transcoding video to HLS!"
            sys.exit(1)

        transcoder.upload_to_s3()
