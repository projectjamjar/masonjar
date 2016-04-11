
from django.test import TestCase
from django.conf import settings
from jamjar.tasks.transcode_video import VideoTranscoder

from jamjar.videos.models import Video, Edge
from jamjar.concerts.models import Concert
from jamjar.venues.models import Venue
from lilo import Lilo

import os
import boto3

from unittest import skip

TEST_VIDEO_PATH_1 = os.path.join(os.path.dirname(__file__), 'in/part1.mp4')
TEST_VIDEO_PATH_2 = os.path.join(os.path.dirname(__file__), 'in/part2.mp4')

TEST_HLS_PATH = os.path.join(os.path.dirname(__file__), 'out/part1.hls')
TEST_TS_PATH = os.path.join(os.path.dirname(__file__), 'out/part10.ts')

class LiloTestCase(TestCase):
    def truncateTestDb(self):
        if 'test' in settings.LILO_CONFIG['database']['db']:
            lilo = Lilo(settings.LILO_CONFIG, None, None)
            lilo.djv.db.empty()
        else:
            raise RuntimeError("trying to truncate a non-test table!")

    def tearDown(self):
        os.remove(TEST_HLS_PATH)
        os.remove(TEST_TS_PATH)
        self.truncateTestDb()

    def setUp(self):
        self.venue = Venue(name="MET Lab", lat=10.0, lng=20.0, website="http://projectjamjar.com", utc_offset=12)
        self.venue.save()

        self.concert = Concert(date="2016-01-01", venue=self.venue)
        self.concert.save()

        self.user = User(username='test', email='test@test.com', first_name='Test', last_name='Test', password='pass')
        self.user.save()

        self.video1 = Video(name="video1", concert_id=self.concert.id, length=10.0, user=self.user)
        self.video1.save()
        
        self.video_transcoder = VideoTranscoder()
        self.truncateTestDb()

    @skip('need to redo this test')
    def test_transcode(self):
        success = self.video_transcoder.transcode_to_hls(TEST_VIDEO_PATH_1, TEST_HLS_PATH)
        self.assertTrue(success, 'Error transcoding video')

        out_dir = os.path.join(os.path.dirname(__file__), 'out')

        uploaded = []
        deleted  = []

        def mocked_upload(s3_path, file_path):
            uploaded.append((s3_path, file_path))

        def mocked_delete(src_dir):
            deleted.append(src_dir)

        self.video_transcoder.do_upload_to_s3 = mocked_upload
        self.video_transcoder.delete_source   = mocked_delete
        self.video_transcoder.upload_to_s3(out_dir)

        self.assertTrue(('test/out/part1.hls', TEST_HLS_PATH) in uploaded)
        self.assertTrue(('test/out/part10.ts', TEST_TS_PATH) in uploaded)
        self.assertTrue(len(uploaded) == 2)

        venue = Venue(name="MET Lab")
        venue.save()

        concert = Concert(date="2016-01-01", venue=venue)
        concert.save()


        v1 = Video(concert_id=concert.id, length=2)
        v1.save()

        v2 = Video(concert_id=concert.id, length=2)
        v2.save()

        length_1 = self.video_transcoder.fingerprint(TEST_VIDEO_PATH_1, v1.id)
        length_2 = self.video_transcoder.fingerprint(TEST_VIDEO_PATH_2, v2.id)

        self.assertTrue(abs(5 - length_1) < .1)
        self.assertTrue(abs(5 - length_2) < .1)

