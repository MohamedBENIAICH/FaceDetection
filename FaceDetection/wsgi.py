"""
WSGI config for FaceDetection project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
<<<<<<< HEAD
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
=======
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
>>>>>>> 96823c6827b23b7a7529a75e690ef3a64981c7b8
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FaceDetection.settings')

application = get_wsgi_application()
