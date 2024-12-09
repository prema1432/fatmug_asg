"""Tasks for extracting subtitles from video files."""

import json
import subprocess

from celery import shared_task
from django.core.files import File

from video_extractor.models.subtitle_model import SubtitleModel
from video_extractor.models.video_model import VideoModel


# pylint: disable=W1510,R1732,W1514


@shared_task
def extract_subtitles_task(video_id):
    """
     Extract subtitles from a video file and save them to the database.

    This task retrieves a video by its ID, uses FFmpeg to extract subtitles
    from the video file, and saves the subtitles in WebVTT format. It also
    updates the video model with the language of the subtitles and stores
    each subtitle entry in the SubtitleModel.

    Args:
        video_id: The ID of the video from which to extract subtitles.

    Returns:
        int: The ID of the video after subtitles have been extracted and saved.

    Raises:
        subprocess.CalledProcessError: If the FFmpeg command fails during execution.
    """
    print("video_idvideo_id : ", video_id)
    video = VideoModel.objects.get(id=video_id)
    print("video : ", video)
    video_path = video.video_file.path

    # Use FFmpeg to extract video information (format and subtitle language)
    probe_command = [
        'ffprobe',
        '-v',
        'error',
        '-show_entries',
        'format=format_name:stream=index,codec_type,codec_name,language',
        '-print_format',
        'json',
        video_path,
    ]

    try:
        print("probe_command : ", probe_command)
        result = subprocess.run(probe_command, capture_output=True, text=True)
        metadata = json.loads(result.stdout)
        print("metadata : ", metadata)
        subtitle_streams = [stream for stream in metadata['streams'] if stream['codec_type'] == 'subtitle']
        if not subtitle_streams:
            return None
        subtitle_language = subtitle_streams[0].get('language',
                                                    'und')

        # Use FFmpeg to extract subtitles (WebVTT format)
        subtitle_output_path = f"{video_path.rsplit('.', 1)[0]}.vtt"
        extract_command = [
            'ffmpeg',
            '-i',
            video_path,
            '-map',
            '0:s:0',
            '-c:s',
            'webvtt',
            subtitle_output_path,
        ]

        # Run the FFmpeg command to extract subtitles
        subprocess.run(extract_command, check=True)

        # Update the video model with the video format and language
        video.language = subtitle_language
        video.subtitle_file.save(f"{video.title}.vtt", File(open(subtitle_output_path, 'rb')))
        video.closed_captions = True
        video.save()

        # Parse WebVTT subtitle file to extract text, start time, and end time
        with open(subtitle_output_path) as subtitle_file:
            subtitles = parse_webvtt(subtitle_file.read())
        # Save each subtitle line as a separate entry in SubtitleModel
        for subtitle in subtitles:
            try:
                SubtitleModel.objects.create(video=video, text=subtitle['text'], start_time=subtitle['start_time'],
                                             end_time=subtitle['end_time'])
            except Exception as e:  # pylint: disable=W0718
                print(f"Error saving subtitle: {e}")
        return video.id
    except subprocess.CalledProcessError as e:  # pylint: disable=W0703
        print(f"Error during subtitle extraction: {e}")
        return None


def parse_webvtt(webvtt_content):
    """
    Parse WebVTT subtitle content into structured subtitle entries.

    This function takes the content of a WebVTT file and extracts individual
    subtitle entries, including their start and end times, as well as the
    corresponding text. It returns a list of dictionaries, each representing
    a subtitle with its timing and text.

    Args:
        webvtt_content: A string containing the raw content of a WebVTT file.

    Returns:
        list: A list of dictionaries, each containing 'start_time', 'end_time',
        and 'text' for each subtitle entry.
    """
    subtitles = []
    lines = webvtt_content.splitlines()
    current_subtitle = {}

    for line in lines:
        if '-->' in line:
            # Extract start and end time
            times = line.split(' --> ')
            current_subtitle['start_time'] = times[0].strip()
            current_subtitle['end_time'] = times[1].strip()
        elif line.strip() == '':
            if current_subtitle:
                subtitles.append(current_subtitle)
                current_subtitle = {}
        else:
            current_subtitle['text'] = current_subtitle.get('text', '') + ' ' + line.strip()

    if current_subtitle:
        subtitles.append(current_subtitle)

    return subtitles
