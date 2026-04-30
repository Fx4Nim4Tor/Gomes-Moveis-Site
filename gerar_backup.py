import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'gomesmoveis'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gomesmoveis.settings')

import django
django.setup()

from django.core import serializers
from django.apps import apps

data = serializers.serialize('json', [obj for model in apps.get_models() for obj in model.objects.all()])

with open('backup.json', 'w', encoding='utf-8') as f:
    f.write(data)

print('Backup gerado!')