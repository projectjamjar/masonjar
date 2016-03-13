from django.conf import settings
from django.utils import timezone
import json, datetime, requests

from jamjar.venues.models import Venue
from jamjar.artists.models import Artist

import spotipy

# Get the logger instance
import logging
logger = logging.getLogger(__name__)

class ServiceError(Exception):
    """
    A generic exception to be used when an issue arises with a service
    """
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return repr(self.message)

class GMapService():
    """
    A service for searching Google Maps things!
    """
    # Config
    api_key = settings.GMAPS_API_KEY
    cache_bust = settings.GMAPS_CACHE_BUST

    # URLs - double-brace the keys that will get replaced later
    places_search_base_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?keyword={{search_term}}&location={{lat}},{{lng}}&radius=15000&key={api_key}'
    place_detail_base_url = 'https://maps.googleapis.com/maps/api/place/details/json?placeid={{place_id}}&key={api_key}'

    # Inject the API key
    places_search_base_url = places_search_base_url.format(api_key=api_key)
    place_detail_base_url = place_detail_base_url.format(api_key=api_key)

    @classmethod
    def search_place(cls,search,lat,lng):
        """
        Attempt to get a location by name and latitude/longitude
        """
        url = cls.places_search_base_url.format(
            search_term=search,
            lat=lat,
            lng=lng
        )

        # Our GET request
        response = requests.get(url)
        data = response.json()

        # Make sure we got some predictions
        if not data.get('results'):
            raise ServiceError('No locations found by name "{}"'.format(search))

        # Get the details of the first place
        place_id = data.get('results')[0].get('place_id')

        return cls.get_place(place_id)

    @classmethod
    def get_place(cls,place_id,use_cache=True):
        # Hit our own database here first to try to get the place
        hit_gmaps = False
        try:
            location = Venue.objects.get(place_id=place_id)
            modified = (timezone.now() - location.modified_at).days
            print modified
            if modified < cls.cache_bust and use_cache:
                logger.info('Venue Cache Hit')
                return location
        except Venue.DoesNotExist, e:
            pass

        # We don't have the location yet, query GMaps
        url = cls.place_detail_base_url.format(
            place_id=place_id
        )

        # Our GET request
        response = requests.get(url, verify=False) # TODO: this is bad!
        data = response.json()

        if data.get('status') == 'INVALID_REQUEST':
            raise ServiceError('A place with id "{}" could not be found.'.format(place_id))

        result = data.get('result')
        address_components = result.get('address_components',[])

        # Attempt to get city, state, and country, returning none if they don't exist
        # We have multiple city types, so try to find them in this order
        city = None
        city_types = ['locality', 'postal_town', 'administrative_area_level_3','sublocality']
        for city_type in city_types:
            # If we haven't found a component which matches a higher priority type, keep lookin'
            if not city:
                city = next(
                    (component.get('long_name') for component in address_components if city_type in component.get('types')),
                    None)

        state,state_short = next(
            ((component.get('long_name'), component.get('short_name')) for component in address_components if 'administrative_area_level_1' in component.get('types')),
            (None,None))
        country, country_short = next(
            ((component.get('long_name'), component.get('short_name')) for component in address_components if 'country' in component.get('types')),
            (None,None))

        location_info = {
            "name": result.get('name',None),
            "formatted_address": result.get('formatted_address',None),
            "lat": result.get('geometry',{}).get('location',{}).get('lat',None),
            "lng": result.get('geometry',{}).get('location',{}).get('lng',None),
            "utc_offset": result.get('utc_offset',None),
            "website": result.get('website',None),
            "city": city,
            "state": state,
            "state_short": state_short,
            "country": country,
            "country_short": country_short
        }

        # Either create or update the object in the database matching this place_id
        location, created = Venue.objects.update_or_create(
            place_id=place_id,
            defaults=location_info
        )

        if not created:
            logger.info('Venue Cache Update')

        return location

    @classmethod
    def update_cache(cls):
        """
        NOTE: This is a utility method and should not be used in production.  I will make one GMaps API call for
        every location in the Venues table
        """
        venue = Venue.objects.all()

        for venue in venues:
            cls.get_place(venue.place_id,use_cache=False)
