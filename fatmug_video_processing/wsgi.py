"""
WSGI config for fatmug_video_processing project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from dj_static import Cling, MediaCling
from django.core.wsgi import get_wsgi_application
from static_ranges import Ranges

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fatmug_video_processing.settings")

application = Ranges(Cling(MediaCling(get_wsgi_application())))
