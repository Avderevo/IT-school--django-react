import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ITS_api.settings')
os.environ.setdefault('DJANGO_CONFIGURATION', 'Dev')
os.environ.setdefault('DJANGO_CONFIGURATION', 'Prod')

from configurations.wsgi import get_wsgi_application

application = get_wsgi_application()