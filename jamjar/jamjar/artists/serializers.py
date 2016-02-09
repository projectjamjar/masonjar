from rest_framework import serializers
from .models import Artist, Genre, ArtistImage

import logging; logger = logging.getLogger(__name__)

class ArtistImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtistImage
        fields = ('url','height','width')

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre

class ArtistSerializer(serializers.ModelSerializer):
    genres = serializers.SerializerMethodField()
    images = ArtistImageSerializer(many=True,required=False)

    class Meta:
        model = Artist
        fields = ('id', 'name', 'spotify_id', 'genres', 'images', 'unofficial')

    def get_genres(self,artist):
        return [genre.name for genre in artist.genres.all()]
