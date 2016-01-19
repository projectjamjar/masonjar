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


urlpatterns = patterns('',

    ########################################
    # Video Views
    ########################################
    url(r'^videos/$', Videos.VideoList.as_view()),
    url(r'^videos/(?P<id>[0-9]+)$', Videos.VideoDetails.as_view()),
    url(r'^videos/stream/(?P<id>.+)$', Videos.VideoStream.as_view()),

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

