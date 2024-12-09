"""Model to store subtitle details."""

from django.db import models

from fatmug_video_processing.utils.time_stamp_model import TimeStampModel
from video_extractor.manangers.subtitle_managers import SubtitleManager
from video_extractor.models.video_model import VideoModel


class SubtitleModel(TimeStampModel):
    """Model to store subtitle details."""

    video = models.ForeignKey(VideoModel, on_delete=models.CASCADE, related_name='subtitles')
    text = models.TextField()
    start_time = models.CharField(max_length=50, null=True, blank=True)
    end_time = models.CharField(max_length=50, null=True, blank=True)

    objects = SubtitleManager()

    def __str__(self):
        """Return string representation of SubtitleModel."""
        return f"{self.video.title}"

    class Meta:
        """Meta class for SubtitleModel."""

        ordering = ['-created_at']
