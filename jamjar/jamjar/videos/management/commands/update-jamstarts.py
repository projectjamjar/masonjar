from django.core.management.base import BaseCommand

from jamjar.tasks.transcode_video import VideoTranscoder
from jamjar.videos.models import Video

class Command(BaseCommand):
    help = 'Recalculate the jamstarts for a jamjar containing video_id'

    def add_arguments(self, parser):
        parser.add_argument('video_id', type=int)

    def handle(self, *args, **options):
        video_id = options['video_id']

        transcoder = VideoTranscoder()
        video = Video.objects.get(pk=video_id)

        transcoder.video = video # hack, sorry
        transcoder.update_jamstarts()
