from django.conf import settings

import uuid
import os

import logging

from jamjar.tasks.transcode_video import transcode_video

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

        self.logger.info("Writing uploaded file to {:}".format(video_filepath))

        with open(video_filepath, 'wb') as output_fh:
            output_fh.write(input_fh.read())

        return video_filepath

    def process_upload(self, input_fh):
        video_uid = uuid.uuid4()

        # do this synchronously
        video_dir  = self.get_video_dir(video_uid)
        tmp_src = self.do_upload(input_fh, video_dir)

        # do this async
        transcode_video.delay(tmp_src, video_dir)

        return tmp_src

