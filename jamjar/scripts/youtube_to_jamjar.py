import sys
from pytube import YouTube
from jamjar.concerts.models import Concert
from jamjar.videos.models import Video

def run():

    for concert in Concert.objects.all():
        artists = ', '.join([a.name for a in concert.artists.all()])

        print '{} - {} @ {} on {}'.format(concert.id,artists,concert.venue.name,concert.date)


    concert_id = int(raw_input('Please enter a concert ID: '))

    concert = Concert.objects.get(pk=concert_id)


    youtube_url = None
    videos = []

    while youtube_url != "":
        youtube_url = raw_input('Paste a YouTube URL (or press ENTER to finish): ')

        if youtube_url != "":
            yt = YouTube(youtube_url)

            print 'Please select one of the following:'

            dees_videos = yt.get_videos()

            for (index, video) in enumerate(dees_videos):
                print '{}.) {} @ {}'.format(index, video.extension, video.resolution)

            index = int(raw_input('Which one?: '))

            video = dees_videos[index]

            videos.append(video)


    print 'Ready to upload {} videos to concert {}'.format(len(videos), concert_id)

    confirm = raw_input('Are you sure (Y/N): ')

    if confirm.lower() != 'y':
        sys.exit(1)

    # for video in videos:

    print "\n\n\nUPLOAD JAWNS COMPLETE :D"
