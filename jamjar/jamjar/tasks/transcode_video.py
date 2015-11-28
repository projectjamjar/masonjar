
from tasks import app

import subprocess
import logging
import os

import boto3


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
    for filename in os.listdir(src_dir):
        disk_path = os.path.join(src_dir, filename)
        s3_path = os.path.join(base_dir, filename)

        # put this in settings
        print "uploading %s to s3://%s" % (disk_path, s3_path)

        s3.Object('jamjar-videos', s3_path).put(Body=open(disk_path, 'rb'))

@app.task(name='tasks.transcode_video')
def transcode_video(src_filepath, out_dir):

    hls_filepath = get_video_filepath(out_dir, 'm3u8')

    transcode_to_hls(src_filepath, hls_filepath)
    upload_to_s3(out_dir)

