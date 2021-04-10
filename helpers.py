def abort_if_video_id_doesnt_exist(video_id):
    if video_id not in videos:
        abort(404, 'not found...')


def abort_if_video_exists(video_id):
    if video_id in videos:
        abort(409, "Video already exisit with that ID")
