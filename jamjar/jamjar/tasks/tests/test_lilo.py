
from django.test import TestCase
from django.conf import settings
from jamjar.tasks.transcode_video import VideoTranscoder

from jamjar.videos.models import Video, Edge
from lilo import Lilo

import os
import boto3

TEST_VIDEO_PATH_1 = os.path.join(os.path.dirname(__file__), 'in/part1.mp4')
TEST_VIDEO_PATH_2 = os.path.join(os.path.dirname(__file__), 'in/part2.mp4')

TEST_HLS_PATH = os.path.join(os.path.dirname(__file__), 'out/part1.hls')
TEST_TS_PATH = os.path.join(os.path.dirname(__file__), 'out/part10.ts')

class LiloTestCase(TestCase):
    @classmethod
    def truncateTestDb(self):
        if 'test' in settings.LILO_CONFIG['database']['db']:
            lilo = Lilo(settings.LILO_CONFIG, None, None)
            lilo.djv.db.empty()
        else:
            raise RuntimeError("trying to truncate a non-test table!")

    @classmethod
    def tearDownClass(cls):
        os.remove(TEST_HLS_PATH)
        os.remove(TEST_TS_PATH)
        cls.truncateTestDb()

    def setUp(self):
        self.video_transcoder = VideoTranscoder()
        self.truncateTestDb()

    def test_transcode(self):
        success = self.video_transcoder.transcode_to_hls(TEST_VIDEO_PATH_1, TEST_HLS_PATH)
        self.assertTrue(success, 'Error transcoding video')

        out_dir = os.path.join(os.path.dirname(__file__), 'out')

        uploaded = []

        def mocked_upload(s3_path, file_path):
            uploaded.append((s3_path, file_path))

        self.video_transcoder.do_upload_to_s3 = mocked_upload
        self.video_transcoder.upload_to_s3(out_dir)

        self.assertTrue(('prod/out/part1.hls', TEST_HLS_PATH) in uploaded)
        self.assertTrue(('prod/out/part10.ts', TEST_TS_PATH) in uploaded)
        #import ipdb; ipdb.set_trace()
        #self.assertTrue(len(uploaded) == 2)

        v1 = Video()
        v1.save()

        v2 = Video()
        v2.save()

        self.video_transcoder.fingerprint(TEST_VIDEO_PATH_1, v1.id)
        self.video_transcoder.fingerprint(TEST_VIDEO_PATH_2, v2.id)

        # TODO : check the edges table
