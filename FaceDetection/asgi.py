<<<<<<< HEAD
"""
ASGI config for FaceDetection project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FaceDetection.settings')

application = get_asgi_application()
=======
# asgi.py
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from FaceDetection import routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FaceDetection.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
        )
    ),
})
>>>>>>> 96823c6827b23b7a7529a75e690ef3a64981c7b8
