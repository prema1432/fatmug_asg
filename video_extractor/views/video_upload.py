"""View for handling video upload and subtitle extraction."""

from django.contrib import messages
from django.shortcuts import redirect, render

from video_extractor.forms.video_forms import VideoUploadForm
from video_extractor.tasks import extract_subtitles_task


def video_upload(request):
    """
    Handle the video upload process and initiate subtitle extraction.

    This function processes a video upload request, validates the uploaded
    video form, and starts the subtitle extraction task if the upload is
    successful. It provides feedback to the user through messages based on
    the outcome of the upload and extraction process.

    Args:
        request: The HTTP request object containing the upload data.

    Returns:
        HttpResponse: A rendered template with the upload form or a redirect
        to the video list upon successful upload.

    Raises:
        Exception: If subtitle extraction fails, an error message is displayed.
    """
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save()
            messages.success(request, 'Video uploaded successfully!')
            try:
                extract_subtitles_task(video.id)
                # extract_subtitles_task(video.id)
                messages.info(request, 'Subtitle extraction started. It may take a few minutes.')
            except Exception as e:  # pylint: disable=broad-exception-caught
                messages.error(request, f'Subtitle extraction failed: {str(e)}')
            return redirect('video_list')
        messages.error(request, 'Error uploading the video. Please check the form and try again.')
        return render(request, 'video_processing/video_upload.html', {'form': form})
    form = VideoUploadForm()
    return render(request, 'video_processing/video_upload.html', {'form': form})
