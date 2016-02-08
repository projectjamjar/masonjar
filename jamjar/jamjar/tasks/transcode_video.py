
from django.conf import settings
from tasks import app
from lilo import Lilo
import subprocess, logging, os, shutil
import boto3, datetime

from jamjar.videos.models import Edge, Video

# extract metadata from videos
from hachoir_core.error import HachoirError
import hachoir_parser, hachoir_metadata

import logging; logger = logging.getLogger(__name__)

class VideoTranscoder(object):
    "Helper class for transcoding, uploading, and fingerprinting"

    def __init__(self):
        self.s3 = boto3.resource('s3')
        self.video = None

    def transcode_to_mp4(self):
        "transcodes an mp4 file to hls"
        src = self.video.tmp_src()
        out = self.video.get_video_filepath('mp4')
        extension = os.path.splitext(self.video.original_filename)[1].lower()
        if extension != '.mp4':
            try:
                with open(os.devnull, "w") as devnull:
                    if extension == '.mov':
                        subprocess.check_call(["avconv", "-i", src, '-c:v', 'libx264', '-c:a', 'copy', '-f', 'mp4', out], stdout=devnull, stderr=devnull)
                    elif extension == '.avi':
                        subprocess.check_call(["avconv", "-i", src, '-c:v', 'libx264', '-crf', '20', '-b:a', '128k', '-strict', 'experimental', '-f', 'mp4', out], stdout=devnull, stderr=devnull)
                    else:
                        subprocess.check_call(["avconv", "-i", src, '-c:v', 'libx264', '-c:a', 'copy', '-f', 'mp4', out], stdout=devnull, stderr=devnull)

                logger.info('Successfully transcoded {:} to {:}'.format(src, out))
                return True
            except subprocess.CalledProcessError:
                # this will retry the job
                #raise RuntimeError('Error transcoding {:} to {:}. Error code: {:}'.format(src, out, result))
                return False
        else:
            # Simply rename the file to mp4
            os.rename(src,out)
            return True

    def transcode_to_hls(self):
        "transcodes an mp4 file to hls"
        src = self.video.get_video_filepath('mp4')
        out = self.video.get_video_filepath('m3u8')

        try:
            with open(os.devnull, "w") as devnull:
              subprocess.check_call(['avconv', '-i', src, '-start_number', '0', '-hls_list_size', '0', '-hls_time', '10', '-f', 'hls', out], stdout=devnull, stderr=devnull)
            logger.info('Successfully transcoded {:} to {:}'.format(src, out))
            return True
        except subprocess.CalledProcessError:
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

    def fingerprint(self):
        "fingerprints an mp4 and inserts the fingerprints into the db"
        video_path = self.video.get_video_filepath('mp4')
        lilo = Lilo(settings.LILO_CONFIG, video_path, self.video.id)
        matched_videos = lilo.recognize_track()

        if matched_videos is not None:
            for match in matched_videos:
                Edge.objects.create(video1_id=self.video.id,video2_id=match['video_id'],offset=match['offset_seconds'],confidence=match['confidence'])

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

        parser = hachoir_parser.createParser(unicode(src))
        if not parser:
            logger.warning("Could not parse file {}".format(src))
            return

        metadata = hachoir_metadata.extractMetadata(parser)

        self.video.width  = metadata.get('width')
        self.video.height = metadata.get('height')
        self.video.recorded_at = metadata.get('creation_date', datetime.datetime.now())

    def run(self, video_id):
        "main entry point to fingerprint, transcode, upload to s3, and delete source dir"

        # Get the video by ID
        self.video = Video.objects.get(pk=video_id)

        # do this before transcoding to get original recording date if available
        self.extract_and_set_metadata()

        # Transcode to mp4 here if needed, otherwise rename video
        if not self.transcode_to_mp4():
             raise RuntimeError('Could not convert video: {} - {}'.format(self.video.name, self.video.uuid))

        # Fingerprint, transcode, and thumbnail the video
        video_length = self.fingerprint()
        self.transcode_to_hls()
        self.extract_thumbnail(video_length)

        # Upload the transcoded videos and thumbnail to S3
        self.upload_to_s3()
        self.delete_source()

        # Update the video length and upload status
        self.video.length = video_length
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

