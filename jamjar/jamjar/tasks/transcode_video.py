
from tasks import app

import subprocess
import logging
import os
import shutil

import boto3

from lilo import Lilo

#from django.conf import settings

def get_video_filepath(video_dir, extension, filename="video"):
    full_filename = '{:}.{:}'.format(filename, extension)
    return os.path.join(video_dir, full_filename)

def transcode_to_hls(src, out):
    logger = logging.getLogger(__name__)
    result = subprocess.check_call(["ffmpeg", "-i", src, '-start_number', '0', '-hls_list_size', '0', '-f', 'hls', out])

    if result == 0:
        logger.info('Successfully transcoded {:} to {:}'.format(src, out))
    else:
        # this will retry the job
        raise RuntimeError('Error transcoding {:} to {:}. Error code: {:}'.format(src, out, result))


def upload_to_s3(src_dir):
    s3 = boto3.resource('s3')

    base_dir = os.path.basename(src_dir)
    s3_dir = os.path.join('prod', base_dir)

    for filename in os.listdir(src_dir):
        disk_path = os.path.join(src_dir, filename)
        s3_path = os.path.join(s3_dir, filename)

        s3.Object('jamjar-videos', s3_path).put(Body=open(disk_path, 'rb'), ACL='public-read')

def delete_source(src_dir):
    shutil.rmtree(src_dir)
    #if settings.VIDEOS_PATH in src_dir:
    #    shutil.rmtree(src_dir)
    #else:
    #    raise RuntimeError("trying to delete dir that shouldn't be deleted!: {:}".format(src_dir))

def fingerprint(src_filepath, video_id):
    lilo = Lilo(src_filepath, video_id)
    matched_videos = lilo.recognize_track()
    for video in matched_videos:
        pass
    lilo.fingerprint_song()

@app.task(name='tasks.transcode_video')
def transcode_video(src_filepath, out_dir, video_id):

    logger = logging.getLogger(__name__)
    logger.info('Trying to transcode video: "{:}" and move to "{:}"'.format(src_filepath, out_dir))

    hls_filepath = get_video_filepath(out_dir, 'm3u8')

    logger.info('HLS Filepath: "{:}"'.format(hls_filepath))

    # TODO : re-enable these... ideally it would use an env variable to determine if it should upload to s3 (don't do it in dev)
    #transcode_to_hls(src_filepath, hls_filepath)
    #upload_to_s3(out_dir)

    fingerprint(src_filepath, video_id)

    #delete_source(out_dir)

