"""Model validators for the video processing app."""

from django.core.exceptions import ValidationError


def validate_video_file(value):
    """Validate the file type of the video."""
    if not value.name.endswith(('.mp4', '.mov', '.avi', '.mkv')):
        raise ValidationError('Invalid file type: only video files are allowed.')
