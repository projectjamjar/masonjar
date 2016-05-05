from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from jamjar.tasks.transcode_video import VideoTranscoder


class Command(BaseCommand):
    help = 'Repeat the upload task for a given video'

    def add_arguments(self, parser):
        parser.add_argument('video_id', type=int)

    def handle(self, *args, **options):
        video_id = options['video_id']

        transcoder = VideoTranscoder()
        transcoder.run(video_id)
