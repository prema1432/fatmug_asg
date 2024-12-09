"""URLs for the video_extractor app."""

from django.urls import path

from video_extractor.views.video_delete_view import video_delete
from video_extractor.views.video_detail_view import video_detail_and_search
from video_extractor.views.video_list_view import video_list
from video_extractor.views.video_upload import video_upload

urlpatterns = [
    path("", video_list, name="video_list"),
    path("video_detail_and_search/<video_id>/", video_detail_and_search, name="video_detail_and_search"),
    path("video_delete/<video_id>/", video_delete, name="video_delete"),
    path("video_upload/", video_upload, name="video_upload"),
]
