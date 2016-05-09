from django.db import models

from jamjar.base.models import BaseModel
from jamjar.videos.models import Edge
from django.db.models import Count

from concert_graph import ConcertGraph

class PopulatedConcertManager(models.Manager):
    def get_queryset(self):
        # don't return concerts with 0 videos in them!
        return super(PopulatedConcertManager, self).get_queryset().annotate(num_videos=Count('videos')).filter(num_videos__gt=0)

class Concert(BaseModel):
    date = models.DateField()
    venue = models.ForeignKey('venues.Venue',related_name='concerts')

    objects = PopulatedConcertManager()

    def make_graph(self):
        concert_id = self.id
        concert_edges = Edge.objects.filter(video1__concert_id=concert_id, video2__concert_id=concert_id).select_related('video1', 'video2')

        g = ConcertGraph(concert_edges)
        return g.disjoint_graphs()
