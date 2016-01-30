
from django.test import TestCase
from django.conf import settings

from jamjar.videos.models import Video, Edge
from jamjar.concerts.models import Concert
from jamjar.venues.models import Venue

import os, logging

TEST_VIDEO_PATH = os.path.join(os.path.dirname(__file__), 'mark-dancing.mp4')

class EdgeTestCase(TestCase):
    def setUp(self):

        venue = Venue(name="MET Lab")
        venue.save()

        concert = Concert(date="2016-01-01", venue=venue)
        concert.save()

        self.video1 = Video(concert_id=concert.id, length=2)
        self.video1.save()

        self.video2 = Video(concert_id=concert.id, length=2)
        self.video2.save()

    def test_edge(self):
        edge = Edge.new(self.video1.id, self.video2.id, 0, 1)
        self.assertTrue(edge.id is not None)

