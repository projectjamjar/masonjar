
from django.conf import settings
from tasks import app
from lilo import Lilo
import subprocess, logging, os, shutil
import boto3

from jamjar.videos.models import Edge, Video

class VideoTranscoder(object):
    "Helper class for transcoding, uploading, and fingerprinting"

    def __init__(self):
        self.production = (settings.JAMJAR_ENV == 'prod')
        self.s3 = boto3.resource('s3')

    def get_video_filepath(self, video_dir, extension, filename="video"):
        "get the relative path for a video"
        full_filename = '{:}.{:}'.format(filename, extension)
        return os.path.join(video_dir, full_filename)

    def transcode_to_hls(self, src, out):
        "transcodes an mp4 file to hls"
        logger = logging.getLogger(__name__)

        try:
            with open(os.devnull, "w") as devnull:
              subprocess.check_call(["ffmpeg", "-i", src, '-start_number', '0', '-hls_list_size', '0', '-f', 'hls', out], stdout=devnull, stderr=devnull)
            logger.info('Successfully transcoded {:} to {:}'.format(src, out))
            return True
        except subprocess.CalledProcessError:
            # this will retry the job
            #raise RuntimeError('Error transcoding {:} to {:}. Error code: {:}'.format(src, out, result))
            return False

    def do_upload_to_s3(self, s3_path, disk_path):
        "helper for uploading to s3 so we can easily mock this in testing"
        self.s3.Object('jamjar-videos', s3_path).put(Body=open(disk_path, 'rb'), ACL='public-read')

    def upload_to_s3(self, out_dir):

        base_dir = os.path.basename(out_dir)
        s3_dir = os.path.join('prod', base_dir)

        for filename in os.listdir(out_dir):
            # TODO : regex here
            if 'mp4' in filename or 'hls' in filename or 'ts' in filename or 'm3u8' in filename:
              disk_path = os.path.join(out_dir, filename)
              s3_path = os.path.join(s3_dir, filename)
              self.do_upload_to_s3(s3_path, disk_path)

    def delete_source(self, src_dir):
        "deletes the source DIRECTORY on disk after uploading to s3"
        if settings.VIDEOS_PATH in src_dir:
            shutil.rmtree(src_dir)
        else:
            raise RuntimeError("trying to delete dir that shouldn't be deleted!: {:}".format(src_dir))

    def fingerprint(self, src_filepath, video_id):
        "fingerprints an mp4 and inserts the fingerprints into the db"
        lilo = Lilo(src_filepath, video_id)
        matched_videos = lilo.recognize_track()

        for match in matched_videos:
            Edge.new(video_id, match['video_id'], video['offset'], video['offset'])

        lilo.fingerprint_song()

    def run(self, src_filepath, out_dir, video_id):
        "main entry point to fingerprint, transcode, upload to s3, and delete source dir"

        hls_filepath = self.get_video_filepath(out_dir, 'm3u8')

        self.fingerprint(src_filepath, video_id)
        self.transcode_to_hls(src_filepath, hls_filepath)

        if self.production:
          self.upload_to_s3(out_dir)
          self.delete_source(out_dir)

        try:
            video = Video.objects.get(id=video_id)
            video.uploaded = True
            video.save()
        except:
          raise RuntimeError("could not update video with id: {:}".format(video_id))

@app.task(name='tasks.transcode_video')
def transcode_video(src_filepath, out_dir, video_id):

    transcoder = VideoTranscoder()

    logger = logging.getLogger(__name__)
    logger.info('Trying to transcode video: "{:}" and move to "{:}"'.format(src_filepath, out_dir))

    transcoder.run(src_filepath, out_dir, video_id)

    logger.info('Done transcoding video: "{:}"'.format(src_filepath, out_dir))
