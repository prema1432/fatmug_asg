"""Admin configuration for the video_extractor app."""

from django.contrib import admin

from video_extractor.models.subtitle_model import SubtitleModel
from video_extractor.models.video_model import VideoModel


@admin.register(SubtitleModel)
class SubtitleAdmin(admin.ModelAdmin):
    """Admin configuration for SubtitleModel."""

    list_display = ('video',)
    search_fields = ('video__title',)


@admin.register(VideoModel)
class VideoAdmin(admin.ModelAdmin):
    """Admin configuration for VideoModel."""

    list_display = ('title', 'closed_captions', 'video_file')
    search_fields = ('title',)
    prepopulated_fields = {'title': ('title',)}
