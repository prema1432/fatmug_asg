"""Video model managers for querying video data."""

from django.db import models


class VideoManager(models.Manager):
    """
    Custom manager for handling video queries.

    This class provides methods to filter videos based on their active status
    and the presence of closed captions. It allows for easy retrieval of
    active, inactive, and captioned videos.

    Methods:
        active: Retrieve all active videos.
        inactive: Retrieve all inactive videos.
        with_closed_captions: Retrieve all active videos that have closed captions.
    """

    def active(self):
        """
        Retrieve all active videos.

        This method filters the video records to return those that are marked
        as active. It allows for easy access to videos that are currently available
        for viewing.

        Returns:
            QuerySet: A queryset of videos that are active.
        """
        return self.filter(is_active=True)

    def inactive(self):
        """
        Retrieve all inactive videos.

        This method filters the video records to return those that are marked
        as inactive. It allows for easy access to videos that are not currently
        available for viewing.

        Returns:
            QuerySet: A queryset of videos that are inactive.
        """
        return self.filter(is_active=False)

    def with_closed_captions(self):
        """
        Retrieve active videos that have closed captions.

        This method filters the active videos to return only those that are
        marked as having closed captions available. It allows for easy access
        to videos that provide additional accessibility features.

        Returns:
            QuerySet: A queryset of active videos that include closed captions.
        """
        return self.active().filter(closed_captions=True)


def search_by_title(self, query):
    """
    Search for active videos by their title.

    This method filters the active videos to find those whose titles contain
    the specified query string, allowing for case-insensitive matching.

    Args:
        query: The string to search for within the video titles.

    Returns:
        QuerySet: A queryset of active videos that match the search criteria.
    """
    return self.active().filter(title__icontains=query)
