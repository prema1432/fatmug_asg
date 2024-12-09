"""Model to store video details."""

from django.db import models

from fatmug_video_processing.utils.model_validators import validate_video_file
from fatmug_video_processing.utils.time_stamp_model import TimeStampModel
from video_extractor.manangers.video_managers import VideoManager


class VideoModel(TimeStampModel):
    """Model to store video details."""

    title = models.CharField(max_length=255)
    video_file = models.FileField(upload_to='videos/', validators=[validate_video_file])
    closed_captions = models.BooleanField(default=False)
    subtitle_file = models.FileField(upload_to='subtitles/', null=True, blank=True)
    language = models.CharField(max_length=50, null=True, blank=True)
    objects = VideoManager()

    def __str__(self):
        """Return string representation of VideoModel."""
        return self.title

    class Meta:
        """Meta class for VideoModel."""

        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['title']),
        ]
