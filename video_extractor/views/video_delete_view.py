"""View for deleting a video from the database."""
from django.contrib import messages
from django.http import Http404, HttpResponseNotAllowed
from django.shortcuts import redirect

from video_extractor.models.video_model import VideoModel


def video_delete(request, video_id):
    """
    Delete a specified video from the database.

    This function handles the deletion of a video when a POST request is made.
    It checks for the existence of the video and, if found, removes it from the
    database, redirecting the user to the video list upon successful deletion.

    Args:
        request: The HTTP request object.
        video_id: The ID of the video to be deleted.

    Returns:
        HttpResponse: A redirect to the video list after deletion.

    Raises:
        Http404: If the video with the specified ID does not exist.
        HttpResponseNotAllowed: If the request method is not POST.
    """
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    # pylint: disable=W0707
    try:
        video = VideoModel.objects.get(id=video_id)
    except VideoModel.DoesNotExist:
        raise Http404("Video does not exist")

    video.delete()
    messages.info(request, f"Video - {video.title} deleted successfully.")
    return redirect('video_list')
