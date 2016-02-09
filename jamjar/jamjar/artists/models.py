from django.db import models
from jamjar.base.models import BaseModel

import spotipy

class Artist(BaseModel):
    name = models.CharField(max_length=150)
    spotify_id = models.CharField(max_length=100, null=True)
    genres = models.ManyToManyField('artists.Genre',related_name='artists',blank=True)
    unofficial = models.BooleanField(default=False)

    @staticmethod
    def search_artist(search_string):
        sp = spotipy.Spotify()

        # Use Spotipy to get the results for the query
        artist_results = sp.search(q=search_string, type='artist',limit=10)

        # Pull out the results that we want for this search and return that
        items = artist_results.get('artists',{}).get('items',[])
        return items

    @classmethod
    def get_or_create_artist(cls, spotify_id):
        # Try to get the artist by spotify_id
        try:
            artist = cls.objects.get(spotify_id=spotify_id)
        except cls.DoesNotExist, e:
            # We don't have this artist in our DB yet.  Get em!
            try:
                sp = spotipy.Spotify()
                spotify_artist = sp.artist(spotify_id)

                if spotify_artist != None:
                    # Create an artist object
                    artist = cls()
                    artist.name = spotify_artist.get('name')
                    artist.spotify_id = spotify_id
                    artist.save()

                    genres = spotify_artist.get('genres',[])
                    for genre in genres:
                        # Get or create the genre and add it
                        (genre, created) = Genre.objects.get_or_create(name=genre)
                        artist.genres.add(genre)

                    images = spotify_artist.get('images',[])
                    for image in images:
                        # Add the image
                        image_obj = ArtistImage.objects.create(artist=artist,**image)
                        artist.images.add(image_obj)

                else:
                    return None
            except IntegrityError, e:
                return None

        return artist


class Genre(models.Model):
    name = models.CharField(max_length=100)

class ArtistImage(BaseModel):
    artist = models.ForeignKey('artists.Artist',related_name='images')
    url = models.URLField(max_length=500)
    width = models.IntegerField()
    height = models.IntegerField()