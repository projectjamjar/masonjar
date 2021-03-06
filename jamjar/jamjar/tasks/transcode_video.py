
from django.conf import settings
from tasks import app
from lilo import Lilo
import subprocess, logging, os, shutil
import boto3, datetime
from celery.contrib import rdb

from django.db.models import Q, Count
from django.db.utils import IntegrityError

from jamjar.videos.models import Edge, Video, JamJarMap

# extract metadata from videos
from hachoir_core.error import HachoirError
import hachoir_parser, hachoir_metadata

# friends don't let friends write their own graph algos :p
import networkx as nx

from ConfigParser import ConfigParser
import StringIO

import logging; logger = logging.getLogger(__name__)

AUDIO_SAMPLE_RATE = '44100'
HLS_SEGMENT_LENGTH_SECONDS = '10' # 10 second .ts files
HLS_MAX_SEGMENTS = '500'          # 10 * 500 = 5000 seconds, or max video length ~= 1.5 hours

MAX_WIDTH = 1024
MAX_HEIGHT = 576
MAX_HLS_WIDTH = 640
MAX_HLS_HEIGHT = 480
MAX_BITRATE = 2 * 1000 * 1000

def GET_BITRATE(src):
    cmd = [settings.AVCONV_PROBE, "-show_streams", src]
    res = subprocess.check_output(cmd)
    buf = StringIO.StringIO(res)

    bit_rate = MAX_BITRATE
    
    parser = ConfigParser({'codec_type': None, 'bit_rate': None})
    parser.readfp(buf)
    
    for section in parser.sections():
        section_type = parser.get(section, "codec_type", None) 
        if section_type == 'video':
           src_bit_rate = parser.get(section, 'bit_rate')
           if src_bit_rate is not None:
               bit_rate =  min(int(float(src_bit_rate)), MAX_BITRATE)
               break

    return bit_rate

def MP4_OPTS(video, src, out):
    output_width = min(video.width, MAX_WIDTH)
    output_height = min(video.height, MAX_HEIGHT)

    bitrate = str(GET_BITRATE(src))

    opts = [
      settings.AVCONV_ENCODER,
      "-y",
      "-i", src,
      "-ar", AUDIO_SAMPLE_RATE,
      "-ac", "2",
      "-codec:v", "libx264",
      "-preset", "slow",
      "-b:v", bitrate,
      "-maxrate:v", bitrate,
      "-bufsize:v", "1000k",
      "-vf", "scale=iw*sar*min({max_width}/(iw*sar)\,{max_height}/ih):ih*min({max_width}/(iw*sar)\,{max_height}/ih),pad={max_width}:{max_height}:(ow-iw)/2:(oh-ih)/2".format(max_width=output_width, max_height=output_height),
    ]

    if settings.JAMJAR_ENV == 'prod':
        opts += [
          "-profile:v", "baseline",
          "-profile:a", "aac_eld",
          "-codec:a", "libfdk_aac",
        ]
    else:
        opts += ["-strict", "experimental"]

    opts += [
      "-b:a", "256k",
      "-movflags", "+faststart",
      "-cutoff", "20000",
      "-f", "mp4",
      out
    ]
    print " ".join(opts)
    return opts

def HLS_OPTS(video, src, out):
    output_width = min(video.width, MAX_HLS_WIDTH)
    output_height = min(video.height, MAX_HLS_HEIGHT)

    opts = [
      settings.AVCONV_ENCODER,
      "-y",
      "-i", src,
      "-codec:v", "libx264",
      "-preset", "slow",
      "-b:v", "500k",
      "-maxrate", "500k",
      "-bufsize", "1000k",
      "-vf", "scale=iw*sar*min({max_width}/(iw*sar)\,{max_height}/ih):ih*min({max_width}/(iw*sar)\,{max_height}/ih),pad={max_width}:{max_height}:(ow-iw)/2:(oh-ih)/2".format(max_width=output_width, max_height=output_height),
    ]


    if settings.JAMJAR_ENV == 'prod':
        opts += [
          "-profile:v", "baseline",
          "-profile:a", "aac_he_v2",
          "-codec:a", "libfdk_aac",
        ]
    else:
        opts += ['-strict', 'experimental']

    opts += [
      "-b:a", "128k",
      "-ss", "0",
      "-t", str(int(video.length)), # TOTAL HACK! AVCONV IS SO FUCKED
      "-start_number", "0",
      "-hls_time", HLS_SEGMENT_LENGTH_SECONDS,
      "-hls_list_size", HLS_MAX_SEGMENTS,
      "-f", "hls",
      out
    ]

    print " ".join(opts)
    return opts


class VideoTranscoder(object):
    "Helper class for transcoding, uploading, and fingerprinting"

    def __init__(self):
        self.s3 = boto3.resource('s3')
        self.video = None

    def transcode_to_mp4(self):
        "transcodes an mp4 file to hls"
        src = self.video.tmp_src()
        out = self.video.get_video_filepath('mp4')

        transcode_stats_prefix = os.path.join(self.video.get_video_dir(), "transcode-stats")
        try:
            logger.info('Running MP4 encoding for video {}'.format(self.video.id))
            subprocess.check_call(MP4_OPTS(self.video, src, out))
            logger.info('Successfully transcoded {:} to {:}'.format(src, out))

            return True
        except subprocess.CalledProcessError as e:
            print e
            # this will retry the job
            #raise RuntimeError('Error transcoding {:} to {:}. Error code: {:}'.format(src, out, result))
            return False

    def transcode_to_hls(self):
        "transcodes an mp4 file to hls"
        src = self.video.get_video_filepath('mp4')
        out = self.video.get_video_filepath('m3u8')

        try:
            logger.info('Running HLS encoding for video {}'.format(self.video.id))
            subprocess.check_call(HLS_OPTS(self.video, src, out))
            logger.info('Successfully transcoded {:} to {:}'.format(src, out))
            return True
        except subprocess.CalledProcessError as e:
            print e
            # this will retry the job
            #raise RuntimeError('Error transcoding {:} to {:}. Error code: {:}'.format(src, out, result))
            return False

    def do_upload_to_s3(self, s3_path, disk_path, content_type):
        "helper for uploading to s3 so we can easily mock this in testing"
        self.s3.Object('jamjar-videos', s3_path).put(Body=open(disk_path, 'rb'), ACL='public-read',ContentType=content_type)

    def upload_to_s3(self):
        local_dir = self.video.get_video_dir()

        content_type_map = {
            '.jpg': 'image/jpeg',
            '.mp4': 'video/mp4',
            '.m3u8': 'application/x-mpegURL',
            '.ts': 'video/MP2T'
        }

        for filename in os.listdir(local_dir):
            extension = os.path.splitext(filename)[1].lower()
            if extension in ['.mp4','.hls','.ts','.m3u8','.jpg']:
                disk_path = os.path.join(local_dir, filename)
                s3_path = os.path.join(settings.JAMJAR_ENV, str(self.video.uuid), filename)
                content_type = content_type_map.get(extension,'binary/octet-stream')
                self.do_upload_to_s3(s3_path, disk_path, content_type=content_type)

    def delete_source(self):
        "deletes the source DIRECTORY on disk after uploading to s3"
        video_dir = self.video.get_video_dir()
        shutil.rmtree(video_dir)

    def update_jamstarts(self):
        concert = self.video.concert

        relevant_edges_query = Q(confidence__gt=settings.CONFIDENCE_THRESHOLD) & Q(video1__concert_id=concert.id) & Q(video2__concert_id=concert.id)
        acyclic_edges_query = Q(video1__is_cycle=False) & Q(video2__is_cycle=False)
        acyclic_relevant_edges = Edge.objects.filter(relevant_edges_query & acyclic_edges_query)

        # unique the resulting edges and make all edges positive
        digraph_edges = []
        seen_video_ids = set()
        for edge in acyclic_relevant_edges:
            video_ids = (edge.video1_id, edge.video2_id)

            if video_ids in seen_video_ids or video_ids[0] == video_ids[1]:
                continue
            else:
                seen_video_ids.add(video_ids)

            # if the edge is negative, flip it! We only want positive edges
            if edge.offset < 0:
                edge.offset *= -1
                edge.video1_id, edge.video2_id = edge.video2_id, edge.video1_id

            edge_data = (int(edge.video2_id), int(edge.video1_id), edge.offset)
            digraph_edges.append(edge_data)

        if len(digraph_edges) == 0:
            # if there are no edges, then we just have to create a jamjar w/ one video (this one) in it
            new_start_id = self.video.id

        else:
            # build a graph from the resulting edges
            digraph = nx.DiGraph()
            video_id = int(self.video.id)
            digraph.add_node(video_id)
            digraph.add_weighted_edges_from(digraph_edges)

            # find all videos in the subgraph
            undirected_graph = digraph.to_undirected()

            video_ids_in_subgraph = nx.node_connected_component(undirected_graph, video_id)

            # check if a cycle exists -- if so: fuck this video
            # if not: continue as normal
            try:
                cycle = nx.find_cycle(digraph)
                # if we get here, a cycle exists, so fuck this video
                new_start_id = self.video.id

                # mark this jamstart as being in a cycle
                self.video.is_cycle = True

            except nx.NetworkXNoCycle:
                # sort the directed graph such that if A has an edge to B, A will come before B in the resulting list
                temporally_sorted_videos = nx.topological_sort(digraph)

                # the first video id in the list is the jamstart for this subgraph
                new_start_id = temporally_sorted_videos[0]

                # update start_id for all videos in the resulting subgraph
                JamJarMap.objects.filter(video_id__in=video_ids_in_subgraph).update(start_id=new_start_id)

        # And add this one
        JamJarMap.objects.create(video=self.video, start_id=new_start_id)

    def update_concert_jamjars_count(self):
        concert = self.video.concert
        jamjars_count = JamJarMap.objects.filter(video__concert_id=concert.id).values('start_id').annotate(num_videos=Count('video_id', distinct=True)).filter(num_videos__gt=1).count()
        concert.jamjars_count = jamjars_count
        concert.save()

    def fingerprint(self):
        "fingerprints an mp4 and inserts the fingerprints into the db"
        video_path = self.video.get_video_filepath('mp4')
        lilo = Lilo(settings.LILO_CONFIG, video_path, self.video.id)
        matched_videos = lilo.recognize_track()

        if matched_videos is not None:
            for match in matched_videos:
                match_data = {"offset": match['offset_seconds'], "confidence": match['confidence']}
                if self.video.id != int(match['video_id']):
                    try:
                        Edge.objects.get_or_create(video1_id=self.video.id, video2_id=match['video_id'], defaults=match_data)
                    except IntegrityError as e:
                        msg = "Could not create edge from {} to {} ({})".format(self.video.id, match['video_id'], e)
                        logger.error(msg)


        # Add this videos fingerprints to the Lilo DB
        data = lilo.fingerprint_song()

        if not data:
            raise RuntimeError('Video already fingerprinted: {} - {}'.format(self.video.name, self.video.uuid))

        return data.get('song_length')

    def extract_thumbnail(self, video_length):
        """
        extracts a thumbnail from a video and uploads it to s3
        Use the following avconv settings
            -i - input video file
            -vsync 1 - video sync method. only write one frame
            -r 1 - writing frame rate.  Use 1 so we only get 1 frame.
            -an - disable audio recording
            -t 1 - stop writing after 1 second
            -ss time - grab the frame at <time> seconds
            -y output - output file
        """
        src = self.video.get_video_filepath('mp4')
        tmp_out = self.video.get_video_filepath('jpg',filename='thumb_orig')
        try:
            with open(os.devnull, "w") as devnull:
                thumbnail_time = video_length/2.0
                # Extract the thumbnail from the video
                subprocess.check_call(['avconv', '-i', src, '-vsync', '1', '-r', '1', '-an', '-t', '1', '-ss', str(thumbnail_time), '-y', tmp_out], stdout=devnull, stderr=devnull)

                # Resize the thumbnail to the appropriate sizes. Filenames will be
                # in the format 'thumb-<size>.jpg' where the image will fit within a <size>x<size> frame
                for size in settings.THUMBNAIL_SIZES:
                    thumb_filename = 'thumb-{}'.format(size)
                    thumb_out = self.video.get_video_filepath('jpg',filename=thumb_filename)
                    size_spec = '{0}x{0}'.format(size)
                    subprocess.check_call(['convert', tmp_out, '-resize', size_spec, thumb_out], stdout=devnull, stderr=devnull)

                logger.info('Successfully extracted and resized thumbnail from {:}'.format(src))
            return True
        except subprocess.CalledProcessError:
            # this will retry the job
            #raise RuntimeError('Error transcoding {:} to {:}. Error code: {:}'.format(src, out, result))
            return False

    def extract_and_set_metadata(self):
        "pull video creation date and dimensions out of video header. This should work for mp4/mov/avi files"
        src = self.video.tmp_src()

        logger.info('Getting metadata for video: "{:}"'.format(src))
        parser = hachoir_parser.createParser(unicode(src))
        if not parser:
            logger.warning("Could not parse file {}".format(src))
            return

        metadata = hachoir_metadata.extractMetadata(parser)


        self.video.width  = metadata.get('width')
        self.video.height = metadata.get('height')
        self.video.length = metadata.get('duration').total_seconds()
        self.video.recorded_at = metadata.get('creation_date', datetime.datetime.now())

    def transcode(self, outputs):
        if 'mp4' in outputs:
            if not self.transcode_to_mp4():
                raise RuntimeError('Could not convert video to mp4: {} - {}'.format(self.video.name, self.video.uuid))
        if 'hls' in outputs:
            if not self.transcode_to_hls():
                raise RuntimeError('Could not convert video to hls: {} - {}'.format(self.video.name, self.video.uuid))

    def run(self, video_id):
        "main entry point to fingerprint, transcode, upload to s3, and delete source dir"

        # Get the video by ID
        self.video = Video.all_objects.get(pk=video_id)

        # do this before transcoding to get original recording date if available
        self.extract_and_set_metadata()

        self.transcode(['mp4', 'hls'])

        # Fingerprint, transcode, and thumbnail the video
        self.fingerprint()

        self.update_jamstarts()
        self.update_concert_jamjars_count()

        self.extract_thumbnail(self.video.length)

        # Upload the transcoded videos and thumbnail to S3
        self.upload_to_s3()
        self.delete_source()

        # relate the artists from this video to the concert
        for artist in self.video.artists.all():
            self.video.concert.artists.add(artist)

        self.video.uploaded = True
        self.video.save()
        # except:
        #   raise RuntimeError("could not update video with id: {:}".format(video_id))

@app.task(name='tasks.transcode_video')
def transcode_video(video_id):

    transcoder = VideoTranscoder()

    logger = logging.getLogger(__name__)
    logger.info('Trying to transcode video: "{:}"'.format(video_id))

    transcoder.run(video_id)

    logger.info('Done transcoding video: "{:}"'.format(video_id))

