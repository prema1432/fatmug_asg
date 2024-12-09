"""Video list view module."""

from django.shortcuts import render

from video_extractor.models.video_model import VideoModel


def video_list(request):
    """
    Retrieve and display a list of active videos.

    This function fetches all active videos from the database and prepares
    them for display in the video list template. It ensures that only videos
    marked as active are shown to the user.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: A rendered template displaying the list of active videos.
    """
    videos = VideoModel.objects.active()

    context = {
        'videos': videos,
    }
    return render(request, 'video_processing/videos_list.html', context)
