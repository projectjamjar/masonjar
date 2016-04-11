
from django.test import TestCase
from django.conf import settings

from jamjar.videos.models import Video

from django.core.files.uploadedfile import UploadedFile

import os

TEST_VIDEO_PATH = os.path.join(os.path.dirname(__file__), 'mark-dancing.mp4')

class UploadTestCase(TestCase):
    def setUp(self):
        self.video = Video(original_filename="video.mp4")

    def test_video_dir(self):
        actual_path = self.video.get_video_dir()
        expected_path = '{:}/{:}'.format(settings.TMP_VIDEOS_PATH, self.video.uuid)
        self.assertEqual(actual_path, expected_path)

    def test_video_filepath(self):

        actual_path = self.video.get_video_filepath("mp4")
        expected_path = '{:}/{:}/{:}'.format(settings.TMP_VIDEOS_PATH, self.video.uuid, 'video.mp4')
        self.assertEqual(actual_path, expected_path)

    def test_video_upload(self):

        # wrap this in an UploadedFile -- this is how it happens in the request!
        input_fh = UploadedFile(file(TEST_VIDEO_PATH, 'r'))
        video_filepath = '/dev/null'


        tmp_src = self.video.process_upload(input_fh)
        #self.assertEqual(video_filepath, res)
