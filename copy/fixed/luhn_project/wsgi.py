"""
WSGI config for luhn_project project.

It exposes the WSGI callable as a module-level variable named `application`.
"""

import os
from django.core.wsgi import get_wsgi_application

# Set default settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'luhn_project.settings')

# Get WSGI application
application = get_wsgi_application()
