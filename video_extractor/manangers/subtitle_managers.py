"""Subtitle manager for the Subtitle model."""

from django.db import models


class SubtitleManager(models.Manager):
    """Custom manager for the Subtitle model."""

    def active(self):
        """
        Retrieve all active subtitles.

        This method filters the subtitle records to return those that are
        marked as active. It allows for easy access to subtitles that are
        currently available for use.

        Returns:
            QuerySet: A queryset of active subtitles.
        """
        return self.filter(is_active=True)

    def inactive(self):
        """
        Retrieve all inactive subtitles.

        This method filters the subtitle records to return those that are
        marked as inactive. It allows for easy access to subtitles that are
        not currently available for use.

        Returns:
            QuerySet: A queryset of inactive subtitles.
        """
        return self.filter(is_active=False)

    def by_language(self, language):
        """
        Retrieve active subtitles filtered by language.

        This method filters the active subtitles to return those that match
        the specified language. It allows for easy access to subtitles in a
        particular language.

        Args:
            language: The language code to filter subtitles by.

        Returns:
            QuerySet: A queryset of active subtitles that match the specified
            language.
        """
        return self.active().filter(language=language)
