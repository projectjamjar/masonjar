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

    # Artists models need to be added here as an optimization so we don't
    # always need to go through the Videos to get them
    artists = models.ManyToManyField('artists.Artist', related_name='concerts')

    # The cached number of jamjars as determined by the jamjar reconciliation process
    jamjars_count = models.IntegerField(default=0)

    # only return concerts w/ > 0 videos in them
    objects = PopulatedConcertManager()

    # return all concerts (useful for video upload)
    all_objects = models.Manager()

    def make_graph(self, user=None):
        concert_id = self.id
        concert_edges = Edge.objects.filter(video1__concert_id=concert_id, video2__concert_id=concert_id)\
                                    .filter(video1__uploaded=True, video2__uploaded=True)\
                                    .filter(video1__is_cycle=False, video2__is_cycle=False)\
                                    .select_related('video1', 'video2')

        if hasattr(user, 'excluded'):
            concert_edges = concert_edges.exclude(video1__user_id__in=user.excluded()).exclude(video2__user_id__in=user.excluded())

        g = ConcertGraph(concert_edges)
        return g.disjoint_graphs()

class SponsoredEvent(BaseModel):
    concert = models.ForeignKey(Concert, related_name='sponsored_event')
    name = models.CharField(max_length=128)
    artists = models.ManyToManyField('artists.Artist', related_name='sponsored_events')

