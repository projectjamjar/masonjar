from collections import defaultdict
from django.conf import settings
from jamjar.videos.models import JamJarMap

class ConcertGraph(object):

    def __init__(self, edges):
        self.edges = edges

    def search(self, video_id, graph, already_seen):
        already_seen.add(video_id)
        edges = graph[video_id]
        for edge in edges:
            next_id = edge['video']
            if next_id not in already_seen:
                self.search(next_id, graph, already_seen)

    def disjoint_graphs(self):
        graph = self.make_graph()

        video_ids = set()
        for edge in self.edges:
            video_ids.add(edge.video1.id)
            video_ids.add(edge.video2.id)

        disjoint_ids = []
        while len(video_ids) > 0:
            video_id  = video_ids.pop()
            found_ids = set()
            self.search(video_id, graph, found_ids) # the ol' python pass-by-reference lol

            video_ids -= found_ids
            disjoint_ids.append(found_ids)

        disjoint_graphs = []
        for id_set in disjoint_ids:
            adjacencies = {}
            for video_id in id_set:
                adjacencies[video_id] = graph[video_id]

            jamstarts = JamJarMap.objects.filter(video_id__in=id_set)
            if len(jamstarts) == 0 or len(adjacencies) <= 1:
                continue
            else:
                start_id = jamstarts[0].start_id

            disjoint_graphs.append({
                "adjacencies": adjacencies,
                "count": len(adjacencies),
                "start_id": start_id
            })

        return disjoint_graphs

    def make_graph(self):
        # create a mapping of video_id --> video for later
        edge_map  = {}
        for edge in self.edges:
            edge_map[(edge.video1.id, edge.video2.id)] = edge

        # build an adjacency list to help with generating the graph
        video_adjacencies = defaultdict(list)
        for edge in self.edges:
            video_adjacencies[edge.video1.id].append(edge.video2.id)
            video_adjacencies[edge.video2.id].append(edge.video1.id)


        graph = {}
        for (video_id, adjacents) in video_adjacencies.iteritems():

            edges = []
            for adj_video_id in adjacents:
                index = (adj_video_id, video_id)
                if index in edge_map:
                    offset = edge_map[index].offset
                    confidence = edge_map[index].confidence
                else:
                    index = index[::-1]
                    offset = -edge_map[index].offset
                    confidence = edge_map[index].confidence

                if confidence <= settings.CONFIDENCE_THRESHOLD:
                    continue

                data = {
                    "video" : adj_video_id,
                    "offset" : offset,
                    "confidence" : confidence
                }

                edges.append(data)

            graph[video_id] = edges

        return graph
