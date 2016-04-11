#!/usr/bin/env python

# annoying -- set this b/c we're circumenting manage.py
import os, sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'jamjar.settings.dev')

sys.path.append("jamjar/")

# annoying -- without this, django says that models aren't ready yet
import django
django.setup()

import autofixture

users = [
    { "id": 1, "password": "pbkdf2_sha256$20000$ebRpMry1r0CY$Jqybz3J8g09jRrUJDgfNC57r4TdQDy44SGmMoCQ+JtI=", "last_login": "2016-03-13 20:34:22", "created_at": "2016-02-04 22:33:21", "modified_at": "2016-02-04 22:33:21", "username": "ethan", "email": "drewbanin+ethan@gmail.com", "first_name": "Ethan", "last_name": "Riback", "is_active": 1, "is_deleted": 0, "first_login": 0, "date_joined": "2016-02-04 22:33:21", "is_staff": 0, "is_superuser": 0 },
    { "id": 2, "password": "pbkdf2_sha256$20000$ebRpMry1r0CY$Jqybz3J8g09jRrUJDgfNC57r4TdQDy44SGmMoCQ+JtI=", "last_login": "2016-03-13 22:35:28", "created_at": "2016-02-04 22:33:21", "modified_at": "2016-02-04 22:33:21", "username": "drew", "email": "drewbanin+drew@gmail.com", "first_name": "Drew", "last_name": "Banin", "is_active": 1, "is_deleted": 0, "first_login": 0, "date_joined": "2016-02-04 22:33:21", "is_staff": 0, "is_superuser": 0 },
    { "id": 3, "password": "pbkdf2_sha256$20000$ebRpMry1r0CY$Jqybz3J8g09jRrUJDgfNC57r4TdQDy44SGmMoCQ+JtI=", "last_login": "2016-03-13 00:14:32", "created_at": "2016-02-04 22:33:21", "modified_at": "2016-02-04 22:33:21", "username": "mark", "email": "drewbanin+mark@gmail.com", "first_name": "Mark", "last_name": "Koh", "is_active": 1, "is_deleted": 0, "first_login": 0, "date_joined": "2016-02-04 22:33:21", "is_staff": 0, "is_superuser": 0 },
    { "id": 4, "password": "pbkdf2_sha256$20000$ebRpMry1r0CY$Jqybz3J8g09jRrUJDgfNC57r4TdQDy44SGmMoCQ+JtI=", "last_login": "2016-03-13 00:14:32", "created_at": "2016-02-04 22:33:21", "modified_at": "2016-02-04 22:33:21", "username": "jess", "email": "drewbanin+jess@gmail.com", "first_name": "Jess", "last_name": "Eng", "is_active": 1, "is_deleted": 0, "first_login": 0, "date_joined": "2016-02-04 22:33:21", "is_staff": 0, "is_superuser": 0 },
    { "id": 5, "password": "pbkdf2_sha256$20000$ebRpMry1r0CY$Jqybz3J8g09jRrUJDgfNC57r4TdQDy44SGmMoCQ+JtI=", "last_login": "2016-03-13 00:14:32", "created_at": "2016-02-04 22:33:21", "modified_at": "2016-02-04 22:33:21", "username": "sanjana", "email": "drewbanin+sanjana@gmail.com", "first_name": "Sanjana", "last_name": "Raj", "is_active": 1, "is_deleted": 0, "first_login": 0, "date_joined": "2016-02-04 22:33:21", "is_staff": 0, "is_superuser": 0 }
]



possible_uuids = [
    '26fbae43-46fe-45fa-aa93-cea87e3c296e',
    '298c28c6-9983-4673-8a0e-4666e418437f',
    '46324b43-01f3-460c-8da9-dab840b1153b'
]

venues = [
    {
        'name': 'Union Transfer', 'place_id': 'ChIJPWg_kNXHxokRPXdE7nqMsI4', 'formatted_address': '1026 Spring Garden St, Philadelphia, PA 19123, United States', 'utc_offset': -300, 'city': 'Philadelphia', 'state': 'Pennsylvania', 'state_short': 'PA', 'country': 'United States', 'country_short': 'US', 'unofficial': False
    },
    {
        'name': 'Mann Center', 'place_id': 'ChIJPWg_kNXHxokRPXdE7nqMsI4', 'formatted_address': '1026 Spring Garden St, Philadelphia, PA 19123, United States', 'utc_offset': -300, 'city': 'Philadelphia', 'state': 'Pennsylvania', 'state_short': 'PA', 'country': 'United States', 'country_short': 'US', 'unofficial': False
    },
    {
        'name': 'Theater of the Living Arts', 'place_id': 'ChIJPWg_kNXHxokRPXdE7nqMsI4', 'formatted_address': '1026 Spring Garden St, Philadelphia, PA 19123, United States', 'utc_offset': -300, 'city': 'Philadelphia', 'state': 'Pennsylvania', 'state_short': 'PA', 'country': 'United States', 'country_short': 'US', 'unofficial': False
    }
]

concerts = [
    {'venue_id': 1, 'date' : '2016-04-01'},
    {'venue_id': 1, 'date' : '2016-04-03'},
    {'venue_id': 2, 'date' : '2016-04-01'},
    {'venue_id': 2, 'date' : '2016-04-05'},
    {'venue_id': 3, 'date' : '2016-04-01'},
    {'venue_id': 3, 'date' : '2016-04-07'},
    {'venue_id': 3, 'date' : '2016-04-10'},
]

genres = ['punk', 'disco', 'rap', 'funk', 'drunk', 'dance', 'k-pop', 'pop', 'top 40']

spotify_ids = ['5INjqkS1o8h1imAzPqGZBb', '1G9G7WwrXka3Z1r7aIDjI7']
artists = ['50 Cent', 'Animal Collective', 'Blood Orange', 'LCD Soundsystem', 'Kurt Vile', 'Amy Winehouse', 'Jamie XX', 'Beck', 'Discovery', 'Cherub', 'Kanye West']

artist_images = [
    { 'url': 'https://i.scdn.co/image/237daa4588d473c1f1b18b6b3dfefc5598bf32c5', 'width': 999, 'height': 666 },
    { 'url': 'https://i.scdn.co/image/e953b712c06d9cdd73f3f4c9a138d487165e8192', 'width': 640, 'height': 427 },
    { 'url': 'https://i.scdn.co/image/a071c3c7c399ed7fdc0eb9d295cccf03346f5914', 'width': 200, 'height': 133 },
    { 'url': 'https://i.scdn.co/image/f538200c33781098d164790a58867b7c7e77ba62', 'width': 64, 'height': 43 }
]


for user in users:
    autofixture.create_one('users.User', field_values=user)

for venue in venues:
    autofixture.create_one('venues.Venue', field_values=venue)

for concert in concerts:
    autofixture.create_one('concerts.Concert', field_values=concert)

for genre in genres:
    autofixture.create_one('artists.Genre', field_values={
        'name': genre,
    })

for artist in artists:
    res = autofixture.create_one('artists.Artist', field_values={
        'name': artist,
        'spotify_id': autofixture.generators.ChoicesGenerator(values=spotify_ids)
    })

    for i in artist_images:
        autofixture.create_one('artists.ArtistImage', field_values={
            'url': i['url'],
            'width': i['width'],
            'height': i['height'],
            'artist': res
        })

autofixture.create('videos.Video', 200, none_p=0, generate_fk=False, follow_m2m=(1,2), field_values={
    "uploaded": True,
    "file_size": autofixture.generators.PositiveIntegerGenerator(),
    "is_private": autofixture.generators.BooleanGenerator(),
    "views": autofixture.generators.PositiveSmallIntegerGenerator(),
    "length": autofixture.generators.PositiveIntegerGenerator(),
    "uuid": autofixture.generators.ChoicesGenerator(values=possible_uuids),
    "name": autofixture.generators.LoremSentenceGenerator(max_length=140),
    "original_filename": autofixture.generators.StringGenerator(max_length=140),
    "height": 1080,
    "width": 1920,
})

autofixture.create('videos.Edge', 200, none_p=0, field_values={
    'offset': autofixture.generators.SmallIntegerGenerator(),
    'confidence': autofixture.generators.PositiveSmallIntegerGenerator()
})
