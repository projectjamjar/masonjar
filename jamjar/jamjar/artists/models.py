from django.db import models, IntegrityError
from jamjar.base.models import BaseModel

import spotipy

import logging
logger = logging.getLogger(__name__)

class Artist(BaseModel):
    name = models.CharField(max_length=150)
    spotify_id = models.CharField(max_length=100, null=True)
    genres = models.ManyToManyField('artists.Genre',related_name='artists',blank=True)
    popularity = models.IntegerField(null=True) # Popularity (0-100) on spotify
    followers = models.IntegerField(null=True) # Number of followers on spotify
    unofficial = models.BooleanField(default=False)

    class Meta:
        # Order artists by popularity
        ordering = ['-popularity']

    def save_spotify_info(self, spotify_artist):
        if spotify_artist != None:
            try:
                # Create an artist object
                self.name = spotify_artist.get('name')
                self.popularity = spotify_artist.get('popularity')
                self.followers = spotify_artist.get('followers',{}).get('total')
                self.genres = [] # Clear out the genres
                self.save()

                genres = spotify_artist.get('genres',[])
                for genre in genres:
                    # Get or create the genre and add it
                    (genre, created) = Genre.objects.get_or_create(name=genre)
                    self.genres.add(genre)

                # Delete all old images
                self.images.all().delete()

                images = spotify_artist.get('images',[])
                for image in images:
                    # Add the image
                    image_obj = ArtistImage.objects.create(artist=self,**image)
                    self.images.add(image_obj)
            except IntegrityError, e:
                logger.warn('Integrity error caught during artist update: {}'.format(e))

    def update_spotify_info(self):
        if self.spotify_id != None:
            try:
                sp = spotipy.Spotify()
                spotify_artist = sp.artist(self.spotify_id)

                # Save that ish to the jawn
                self.save_spotify_info(spotify_artist)

            except spotipy.SpotifyException, e:
                logger.warn('Spotify error caught during artist update: {}'.format(e))

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
            # NOTE: We need to be careful of race conditions here!!!
            try:
                sp = spotipy.Spotify()
                spotify_artist = sp.artist(spotify_id)

                if spotify_artist != None:
                    # Create an artist object
                    artist = cls()
                    artist.spotify_id = spotify_id
                    artist.save()

                    # Save that sweet, sweet, spotify info
                    artist.save_spotify_info(spotify_artist)
                else:
                    return None
            except IntegrityError, e:
                logger.warn('Integrity error caught during artist creation: {}'.format(e))
                return None
            except spotipy.SpotifyException, e:
                logger.warn('Spotify error caught during artist creation: {}'.format(e))
                return None

        return artist


class Genre(models.Model):
    name = models.CharField(max_length=100)

class ArtistImage(BaseModel):
    artist = models.ForeignKey('artists.Artist',related_name='images')
    url = models.URLField(max_length=500)
    width = models.IntegerField()
    height = models.IntegerField()
