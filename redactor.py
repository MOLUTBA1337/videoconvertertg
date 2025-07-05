from moviepy import VideoFileClip
from moviepy.video.fx.Crop import Crop
import os

def redact_video(id):
    input_filename1 = f"media/{id}_input_video.mp4"
    file_size = os.path.getsize(input_filename1)

    if file_size/(2**20) > 20:
        return '<b>К сожалению телеграмм может скачивать файлы не более 20мб.</b>'

    else:

        input_filename = f"media/{id}_input_video.mp4"
        output_filename = f"media/{id}_output_video.mp4"

        clip = VideoFileClip(input_filename)

        max_duration = 60
        if clip.duration >= max_duration:
            clip = clip.subclipped(0, max_duration)


        size = min(clip.w, clip.h)
        x_center = clip.w / 2
        y_center = clip.h / 2

        obrclip = Crop(
            x_center=x_center,
            y_center=y_center,
            width=size,
            height=size
        )
        clip = obrclip.apply(clip)


        clip = clip.resized((384, 384))

        clip.write_videofile(
            output_filename,
            codec='libx264',
            audio_codec='aac',
            remove_temp=True,
            threads=4,
            logger=None
        )
        clip.close()
