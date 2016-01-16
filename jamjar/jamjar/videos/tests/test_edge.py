
from django.test import TestCase
from django.conf import settings

from jamjar.videos.models import Video, Edge

import os, logging

TEST_VIDEO_PATH = os.path.join(os.path.dirname(__file__), 'mark-dancing.mp4')

class EdgeTestCase(TestCase):
    def setUp(self):
        self.video1 = Video()
        self.video1.save()

        self.video2 = Video()
        self.video2.save()

    def test_edge(self):
        edge = Edge.new(self.video1.id, self.video2.id, 0, 1)
        self.assertTrue(edge.id is not None)

