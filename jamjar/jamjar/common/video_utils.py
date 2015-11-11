from django.conf import settings

import subprocess
import uuid
import os

import logging

class VideoUtils(object):
    BASE_PATH = settings.VIDEOS_PATH

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def get_video_dir(self, uuid):
        return '{:}/{:}'.format(VideoUtils.BASE_PATH, uuid)

    def get_video_filepath(self, video_dir, extension, filename="video"):
        full_filename = '{:}.{:}'.format(filename, extension)
        return os.path.join(video_dir, full_filename)

    def do_upload(self, input_fh, output_dir):
        os.makedirs(output_dir) # video path is {BASE}/{uuid}/video.mp4

        video_filepath = self.get_video_filepath(output_dir, 'mp4')

        print "Writing uploaded file to {:}".format(video_filepath)

        with open(video_filepath, 'wb') as output_fh:
            output_fh.write(input_fh.read())

        return video_filepath

    def encode_to_hls(self, src_video_filepath, hls_video_filepath):

        result = subprocess.check_call(["ffmpeg", "-i", src_video_filepath, '-start_number', '0', '-hls_list_size', '0', '-f', 'hls', hls_video_filepath])

        if result == 0:
            self.logger.info('Successfully transcoded {:} to {:}'.format(src_video_filepath, hls_video_filepath))
        else:
            # should this raise?
            self.logger.error('Error transcoding {:} to {:}. Error code: {:}'.format(src_video_filepath, hls_video_filepath, result))

    def upload_file(self, input_fh):
        video_uid = uuid.uuid4()

        video_dir = self.get_video_dir(video_uid)
        src_video_filepath = self.do_upload(input_fh, video_dir)

        hls_video_filepath = self.get_video_filepath(video_dir, 'm3u8')
        self.encode_to_hls(src_video_filepath, hls_video_filepath)

        return {
            "uid": video_uid,
            "dir": video_dir,
            "src": src_video_filepath,
            "hls": hls_video_filepath
        }


