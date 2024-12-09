"""Forms for video_extractor app."""

from django import forms

from video_extractor.models.video_model import VideoModel


class VideoUploadForm(forms.ModelForm):
    """Form to upload video."""

    video_file = forms.FileField(
        label='Select a video file',
        widget=forms.ClearableFileInput(attrs={'accept': '.mp4, .mkv'})
    )

    class Meta:
        """Meta class for VideoUploadForm."""

        model = VideoModel
        fields = ['title', 'video_file']
