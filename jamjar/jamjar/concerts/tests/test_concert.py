
from django.test import TestCase
from django.conf import settings

from jamjar.videos.models import Video, Edge
from jamjar.concerts.models import Concert
from jamjar.venues.models import Venue

import os, logging

class ConcertTestCase(TestCase):
    def setUp(self):
        self.venue = Venue(name="MET Lab", lat=10.0, lng=20.0, website="http://projectjamjar.com", utc_offset=12)
        self.venue.save()

        self.concert = Concert(date="2016-01-01", venue=self.venue)
        self.concert.save()

        self.video1 = Video(name="video1", concert_id=self.concert.id, length=10.0)
        self.video1.save()

        self.video2 = Video(name="video2", concert_id=self.concert.id, length=10.0)
        self.video2.save()

        self.video3 = Video(name="video3", concert_id=self.concert.id, length=10.0)
        self.video3.save()

        self.edge1 = Edge.new(video1_id=self.video1.id, video2_id=self.video2.id, confidence=10, offset=20.0)
        self.edge2 = Edge.new(video1_id=self.video2.id, video2_id=self.video3.id, confidence=11, offset=10.0)
        self.edge3 = Edge.new(video1_id=self.video1.id, video2_id=self.video3.id, confidence=12, offset=30.0)

    def test_graph_generation(self):
        graph = self.concert.make_graph()


        self.assertEqual(len(graph), 3)
        self.assertEqual(sorted([i['video']['name'] for i in graph]), ['video1', 'video2', 'video3'])

        for item in graph:
            self.assertEqual(len(item['connects_to']), 2)
            self.assertTrue(item['video']['id'] not in [j['video']['id'] for j in item['connects_to']])

            for connection in item['connects_to']:
                self.assertTrue('confidence' in connection['edge'])
                self.assertTrue('offset' in connection['edge'])

