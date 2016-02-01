from django.db import models
from django.forms.models import model_to_dict

from jamjar.base.models import BaseModel
from jamjar.videos.models import Edge

from collections import defaultdict

class Concert(BaseModel):
    date = models.DateField()
    venue = models.ForeignKey('venues.Venue',related_name='concerts')

    def make_graph(self):
        concert_id = self.id
        concert_edges = Edge.objects.filter(video1__concert_id=concert_id).select_related('video1', 'video2')

        # create a mapping of video_id --> video for later
        video_map = {}
        edge_map  = {}
        for edge in concert_edges:
            video_map[edge.video1.id] = edge.video1
            video_map[edge.video2.id] = edge.video2

            edge_map[(edge.video1.id, edge.video2.id)] = edge

        # build an adjacency list to help with generating the graph
        video_adjacencies = defaultdict(list)
        for edge in concert_edges:
            video_adjacencies[edge.video1.id].append(edge.video2)
            video_adjacencies[edge.video2.id].append(edge.video1)

        graph = []
        for (video_id, adjacents) in video_adjacencies.iteritems():
            video = video_map[video_id]

            connects_to = []
            for adj_video in adjacents:
                index = (adj_video.id, video_id)
                if index in edge_map:
                    offset = edge_map[index].offset
                    confidence = edge_map[index].confidence
                elif index[::-1] in edge_map:
                    index = index[::-1]
                    offset = -edge_map[index].offset
                    confidence = edge_map[index].confidence
                else:
                    raise RuntimeError("this shouldn't happen")

                data = {
                    "video" : model_to_dict(adj_video),
                    "edge"  : {
                        "offset" : offset,
                        "confidence" : confidence
                    }
                }
                connects_to.append(data)

            data = {
                "video": model_to_dict(video),
                "conncects_to" : connects_to
            }
            graph.append(data)

        return graph
