"""View for retrieving video details and searching for matching subtitles."""

from django.http import Http404
from django.shortcuts import render

from video_extractor.models.video_model import VideoModel


def video_detail_and_search(request, video_id):
    """
     Retrieve video details and search for matching subtitles.

    This function fetches the details of a specific video based on its ID
    and allows for searching subtitles that match a given query. If matching
    subtitles are found, their start and end times are also provided for
    further context.

    Args:
        request: The HTTP request object containing the search query.
        video_id: The ID of the video to retrieve.

    Returns:
        HttpResponse: A rendered template displaying the video details and
        any matching subtitles.

    Raises:
        Http404: If the video with the specified ID does not exist.
    """
    # pylint: disable=W0707
    try:
        video = VideoModel.objects.get(id=video_id)
    except VideoModel.DoesNotExist:
        raise Http404("Video does not exist")

    query = request.GET.get('q', '').lower()
    matching_subtitles = []
    start_time = None
    end_time = None

    if query:
        matching_subtitles = video.subtitles.filter(text__icontains=query).order_by('start_time')
        if matching_subtitles.exists():
            start_time = matching_subtitles.first().start_time
            end_time = matching_subtitles.last().end_time

    context = {
        'video': video,
        'matching_subtitles': matching_subtitles,
        'query': query,
        'start_time': start_time,
        'end_time': end_time,
    }

    return render(request, 'video_processing/video_detail.html', context)
