
from tasks import app

import subprocess
import logging


@app.task(name='tasks.transcode_video')
def transcode_video(src_video_filepath, hls_video_filepath):
  logger = logging.getLogger(__name__)
  result = subprocess.check_call(["ffmpeg", "-i", src_video_filepath, '-start_number', '0', '-hls_list_size', '0', '-f', 'hls', hls_video_filepath])

  if result == 0:
    logger.info('Successfully transcoded {:} to {:}'.format(src_video_filepath, hls_video_filepath))
  else:
    # should this raise?
    logger.error('Error transcoding {:} to {:}. Error code: {:}'.format(src_video_filepath, hls_video_filepath, result))
