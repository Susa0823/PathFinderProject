"""
WSGI config for PathFinder project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# ! waitress-serve PathFinder.PathFinderBase.wsgi:application
# Since apparently gunicorn is not available on windows
# gunicorn --bind 0.0.0.0:8000 myproject.wsgi on remote eventually
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'PathFinder.PathFinderBase.settings')

application = get_wsgi_application()
