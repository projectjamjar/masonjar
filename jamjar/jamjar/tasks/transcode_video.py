from tasks import app

import jamjar.common.video_utils

@app.task
def run(src_video_filepath, hls_video_filepath):
    video_utils = video_utils.VideoUtils()
    video_utils.encode_to_hls(src_video_filepath, hls_video_filepath)
