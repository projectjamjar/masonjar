from django.db import models

from jamjar.base.models import BaseModel
from jamjar.videos.models import Edge

from concert_graph import ConcertGraph

class Concert(BaseModel):
    date = models.DateField()
    venue = models.ForeignKey('venues.Venue',related_name='concerts')


    def make_graph(self):
        concert_id = self.id
        concert_edges = Edge.objects.filter(video1__concert_id=concert_id, video2__concert_id=concert_id).select_related('video1', 'video2')

        g = ConcertGraph(concert_edges)
        return g.disjoint_graphs()
