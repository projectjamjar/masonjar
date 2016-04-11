
from django.test import TestCase
from django.conf import settings

from jamjar.videos.models import Video, Edge
from jamjar.concerts.models import Concert
from jamjar.venues.models import Venue
from jamjar.users.models import User

import os, logging

TEST_VIDEO_PATH = os.path.join(os.path.dirname(__file__), 'mark-dancing.mp4')

class EdgeTestCase(TestCase):
    def setUp(self):
        self.venue = Venue(name="MET Lab", lat=10.0, lng=20.0, website="http://projectjamjar.com", utc_offset=12)
        self.venue.save()

        self.concert = Concert(date="2016-01-01", venue=self.venue)
        self.concert.save()

        self.user = User(username='test', email='test@test.com', first_name='Test', last_name='Test', password='pass')
        self.user.save()

        self.video1 = Video(concert_id=self.concert.id, length=10.0, user=self.user)
        self.video1.save()

        self.video2 = Video(concert_id=self.concert.id, length=10.0, user=self.user)
        self.video2.save()

        self.video3 = Video(concert_id=self.concert.id, length=10.0, user=self.user)
        self.video3.save()

        self.edge1 = Edge.new(video1_id=self.video1.id, video2_id=self.video2.id, confidence=10, offset=20.0)
        self.edge2 = Edge.new(video1_id=self.video2.id, video2_id=self.video3.id, confidence=11, offset=10.0)
        self.edge3 = Edge.new(video1_id=self.video1.id, video2_id=self.video3.id, confidence=12, offset=30.0)

    def test_edge(self):
        edge = Edge.new(self.video1.id, self.video2.id, 0, 1)
        self.assertTrue(edge.id is not None)

