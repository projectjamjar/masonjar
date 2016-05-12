"""jamjar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, patterns, url
from django.contrib import admin

import jamjar.videos.views as Videos
import jamjar.authentication.views as Auth
import jamjar.concerts.views as Concerts
import jamjar.artists.views as Artists
import jamjar.venues.views as Venues
import jamjar.search.views as Search
import jamjar.users.views as Users


urlpatterns = patterns('',

    ########################################
    # Search Views
    ########################################
    url(r'^search/$', Search.SearchResults.as_view()),

    ########################################
    # Video Views
    ########################################
    url(r'^videos/$', Videos.VideoListView.as_view()),
    url(r'^videos/flags/$', Videos.VideoFlagView.as_view()),
    url(r'^videos/vote/$', Videos.VideoVoteView.as_view()),
    url(r'^videos/jampicks/$', Videos.JamPickView.as_view()),
    url(r'^videos/(?P<id>[0-9]+)/$', Videos.VideoDetailsView.as_view()),
    url(r'^videos/(?P<id>[0-9]+)/watching/$', Videos.VideoWatchView.as_view()),


    ########################################
    # Concert Views
    ########################################
    url(r'^concerts/$', Concerts.ConcertListView.as_view()),
    url(r'^concerts/(?P<id>[0-9]+)/$', Concerts.ConcertDetailView.as_view()),
    url(r'^concerts/sponsored/$', Concerts.SponsoredEventView.as_view()),

    ########################################
    # Artist Views
    ########################################
    url(r'^artists/search/(?P<search_string>.+)/$', Artists.ArtistSearchView.as_view()),
    url(r'^artists/$', Artists.ArtistListView.as_view()),
    url(r'^genres/$', Artists.GenreView.as_view()),

    ########################################
    # Venue Views
    ########################################
    url(r'^venues/search/(?P<search_string>.+)/$', Venues.VenueSearchView.as_view()),

    ########################################
    # User Views
    ########################################
    url(r'^users/(?P<username>.+)/$', Users.UserProfileView.as_view()),

    ########################################
    # Auth Views
    ########################################
    url(r'^auth/signup/$', Auth.SignupView.as_view()),
    url(r'^auth/activate/$', Auth.ActivateView.as_view()),
    url(r'^auth/login/$', Auth.LoginView.as_view()),
    url(r'^auth/reset/$', Auth.ResetView.as_view()),
    url(r'^change/$', Auth.ChangePasswordView.as_view()),
    url(r'^invite/$', Auth.InviteUserView.as_view()),
)

