
from django.test import TestCase
from django.conf import settings
from jamjar.tasks.transcode_video import VideoTranscoder

import os
import boto3

TEST_VIDEO_PATH = os.path.join(os.path.dirname(__file__), 'in/mark-dancing.mp4')

TEST_HLS_PATH = os.path.join(os.path.dirname(__file__), 'out/mark-dancing.hls')
TEST_TS_PATH = os.path.join(os.path.dirname(__file__), 'out/mark-dancing0.ts')

class LiloTestCase(TestCase):
    def setUp(self):
        self.video_transcoder = VideoTranscoder()

    @classmethod
    def tearDownClass(cls):
        os.remove(TEST_HLS_PATH)
        os.remove(TEST_TS_PATH)

    def test_import(self):
        from lilo import Lilo # just make sure the lib is included correctly

    def test_transcode(self):
        success = self.video_transcoder.transcode_to_hls(TEST_VIDEO_PATH, TEST_HLS_PATH)
        self.assertTrue(success, 'Error transcoding video')

        out_dir = os.path.join(os.path.dirname(__file__), 'out')

        uploaded = []

        def mocked_upload(s3_path, file_path):
            uploaded.append((s3_path, file_path))

        self.video_transcoder.do_upload_to_s3 = mocked_upload
        self.video_transcoder.upload_to_s3(out_dir)

        #import pdb; pdb.set_trace()
        self.assertTrue(('prod/out/mark-dancing.hls', TEST_HLS_PATH) in uploaded)
        self.assertTrue(('prod/out/mark-dancing0.ts', TEST_TS_PATH) in uploaded)
        self.assertTrue(len(uploaded) == 2)
