
from django.test import TestCase
from django.conf import settings

from jamjar.videos.models import Video

from django.core.files.uploadedfile import UploadedFile

import os

TEST_VIDEO_PATH = os.path.join(os.path.dirname(__file__), 'mark-dancing.mp4')

class UploadTestCase(TestCase):
    def setUp(self):
        self.video = Video()

    def test_video_dir(self):
        vuid = "abcdef-1234567890-abcdef"

        actual_path = self.video.get_video_dir(vuid)
        expected_path = '{:}/{:}'.format(settings.VIDEOS_PATH, vuid)
        self.assertEqual(actual_path, expected_path)

    def test_video_filepath(self):

        actual_path = self.video.get_video_filepath("/home/videos", "mp4", "my-video")
        expected_path = '/home/videos/my-video.mp4'
        self.assertEqual(actual_path, expected_path)

    def test_video_upload(self):

        # wrap this in an UploadedFile -- this is how it happens in the request!
        input_fh = UploadedFile(file(TEST_VIDEO_PATH, 'r'))
        video_filepath = '/dev/null'

        res = self.video.do_upload(input_fh, video_filepath)
        self.assertEqual(video_filepath, res)
