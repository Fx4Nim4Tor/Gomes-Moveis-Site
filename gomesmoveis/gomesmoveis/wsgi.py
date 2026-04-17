# """
# WSGI config for gomesmoveis project.

# It exposes the WSGI callable as a module-level variable named ``application``.

# For more information on this file, see
# https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/a
# """

# import os

# from django.core.wsgi import get_wsgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gomesmoveis.settings')

# application = get_wsgi_application()

import os
import sys
from pathlib import Path

# adiciona a pasta do projeto no path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gomesmoveis.settings')

application = get_wsgi_application()

# Vercel precisa dessa variável
app = application