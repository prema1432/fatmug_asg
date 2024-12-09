"""This module contains the TimeStampModel class."""
import uuid

from django.db import models


class TimeStampModel(models.Model):
    """Abstract model to store timestamp details."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        """Meta class for TimeStampModel."""

        abstract = True
