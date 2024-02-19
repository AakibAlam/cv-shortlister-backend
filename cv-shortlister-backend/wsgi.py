import os

from django.core.wsgi import get_wsgi_application

settings_module = 'cv-shortlister-backend.production' if 'WEBSITE_HOSTNAME' in os.environ else 'cv-shortlister-backend.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

application = get_wsgi_application()
