import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'gomesmoveis'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gomesmoveis.settings')

import django
from django.conf import settings
settings.DATABASES['default'] = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': os.path.join(os.path.dirname(__file__), 'gomesmoveis', 'db.sqlite3'),
}

django.setup()

from django.core import serializers
from core.models import Categoria

data = serializers.serialize('json', Categoria.objects.all(), ensure_ascii=False)

with open('categorias.json', 'w', encoding='utf-8') as f:
    f.write(data)

print(f'Categorias exportadas: {Categoria.objects.count()}')