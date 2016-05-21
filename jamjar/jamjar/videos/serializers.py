from rest_framework import serializers
from django.db.models import Q, Count
from jamjar.videos.models import Video, Edge, JamJarMap, VideoFlag, VideoVote
from jamjar.artists.serializers import ArtistSerializer
from jamjar.users.serializers import UserSerializer
from jamjar.artists.models import Artist
from jamjar.concerts.concert_graph import ConcertGraph
from jamjar.concerts.models import Concert

import os

class VideoSerializer(serializers.ModelSerializer):
    artists = ArtistSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)
    votes = serializers.SerializerMethodField()
    concert = serializers.PrimaryKeyRelatedField(queryset=Concert.all_objects)

    class Meta:
        model = Video
        fields = ('id',
                  'name',
                  'uploaded',
                  'created_at',
                  'uuid',
                  'length',
                  'file_size',
                  'is_private',
                  'views',
                  'artists',
                  'web_src',
                  'hls_src',
                  'thumb_src',
                  'concert',
                  'user',
                  'width',
                  'height',
                  'votes')

    def __init__(self, *args, **kwargs):
        super(VideoSerializer, self).__init__(*args, **kwargs)

    def validate(self, data):
        request = self.context.get('request')
        data['user_id'] = request.token.user_id
        input_fh = self.context.get('request').FILES.get('file')

        # Get the artists from the request!
        if request.data.get('artists'):
            artists = request.data.getlist('artists')
            # Get the artist objects and filter out the Nones if there are any
            data['artist_objects'] = [artist for artist in [Artist.get_or_create_artist(artist) for artist in artists] if artist]

        if not input_fh:
            raise serializers.ValidationError('No file given')

        if not input_fh.name:
            raise serializers.ValidationError('File unnamed?')

        extension = os.path.splitext(input_fh.name)[1].lower()

        if extension not in ['.mp4','.avi','.mov']:
            raise serializers.ValidationError('Unacceptable file type: {}'.format(extension))

        # Create the filename and size with the file
        data['original_filename'] = input_fh.name
        data['file_size'] = input_fh.size
        data['file'] = input_fh

        return data

    def create(self,validated_data):
        # Get the artists out of here beforehand
        artists = validated_data.pop('artist_objects',[])

        # Call the super's 'create'

        video = super(VideoSerializer,self).create(validated_data)

        # Assign the artists to the video
        video.artists = artists

        return video

    def get_votes(self, obj):
        request = self.context.get('request', None)

        # group by vote type and return COUNT(vote)
        video_votes = list(obj.votes.all().values('vote').annotate(total=Count('vote')))

        # remove vote types which are already present in response
        possible_vote_types = [True, False, None]
        for vote in video_votes:
            if vote['vote'] in possible_vote_types:
                vote_idx = possible_vote_types.index(vote['vote'])
                possible_vote_types.pop(vote_idx)

        # add missing vote types
        for vote_type in possible_vote_types:
            video_votes.append({'vote': vote_type, 'total': 0})

        if request.user.is_anonymous():
            user_vote = None
        else:
            # get the vote for the logged in user
            user_votes = obj.votes.filter(user=request.user)
            user_vote = user_votes[0].vote if len(user_votes) > 0 else None

        return {
            'user_vote': user_vote,
            'video_votes': video_votes
        }



class ExpandedVideoSerializer(VideoSerializer):

    class Meta:
        model = Video
        fields = ('id',
                  'name',
                  'uploaded',
                  'created_at',
                  'uuid',
                  'length',
                  'file_size',
                  'is_private',
                  'views',
                  'artists',
                  'web_src',
                  'hls_src',
                  'thumb_src',
                  'concert',
                  'user',
                  'width',
                  'height',
                  'votes')

    def __init__(self, *args, **kwargs):
        super(ExpandedVideoSerializer, self).__init__(*args, **kwargs)

        from jamjar.concerts.serializers import ConcertSerializer
        self.fields['concert'] = ConcertSerializer(read_only=True)

class JamJarVideoSerializer(ExpandedVideoSerializer):
    jamjar = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = ('id',
                  'name',
                  'uploaded',
                  'created_at',
                  'uuid',
                  'length',
                  'file_size',
                  'is_private',
                  'views',
                  'artists',
                  'web_src',
                  'hls_src',
                  'thumb_src',
                  'concert',
                  'user',
                  'width',
                  'height',
                  'jamjar',
                  'votes')

    def __init__(self, *args, **kwargs):
        super(JamJarVideoSerializer, self).__init__(*args, **kwargs)

        from jamjar.concerts.serializers import ConcertSerializer
        self.fields['concert'] = ConcertSerializer(read_only=True)

    def get_jamjar(self, obj):
        # Get the startjar of this video
        start_id = obj.jamjars.first().start.id

        # Get all the other videos that start with this startjar

        request = self.context.get('request')
        jamjar_videos = Video.objects.for_user(request.user).filter(jamjars__start_id=start_id)
        # import ipdb;ipdb.set_trace()

        # Serialize all those videos
        jamjar_video_data = VideoSerializer(jamjar_videos,many=True, context=self.context).data

        # Build the graph for the jawn
        edges = Edge.objects.filter(Q(video1__jamjars__start_id=start_id), Q(video2__jamjars__start_id=start_id))

        # edge_data = EdgeSerializer(edges, many=True).data

        graphs = ConcertGraph(edges).disjoint_graphs()

        if len(graphs) > 0:
            graph = graphs[0]
        else:
            graph = None

        jamjar_data = {
            'start': start_id,
            'videos': jamjar_video_data,
            'graph': graph
        }

        return jamjar_data

class EdgeSerializer(serializers.ModelSerializer):
    video1 = VideoSerializer(read_only=True)
    video2 = VideoSerializer(read_only=True)

    class Meta:
        model = Edge
        fields = ('id', 'video1', 'video2', 'offset', 'confidence')

class VideoFlagSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = VideoFlag
        fields = ('id','video','user','flag_type','notes')

    def validate(self, data):
        request = self.context.get('request')
        data['user_id'] = request.token.user_id

        return data

class VideoVoteSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = VideoVote
        fields = ('video','user','vote')

    def validate(self, data):
        request = self.context.get('request')
        data['user_id'] = request.token.user_id

        return data
