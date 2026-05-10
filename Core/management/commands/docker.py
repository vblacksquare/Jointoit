
import pandas as pd
from pathlib import Path
from config import get_config

from django.core.management.base import BaseCommand
from django.conf import settings


CONFIG = get_config()


class Command(BaseCommand):
    help = 'Generate docker-compose.yml'

    def compose(self):
        template_path = Path(settings.BASE_DIR) / 't-docker-compose.yml'
        with open(template_path, "r") as f:
            template_data = f.read()

        self.stdout.write(self.style.HTTP_INFO(f'Found template {template_path}'))

        config_data = pd.json_normalize(CONFIG.model_dump(), sep='_').to_dict(orient='records')[0]
        data = template_data.format(**config_data)

        output_path = Path(settings.BASE_DIR) / 'docker-compose.yml'
        with open(output_path, 'w') as f:
            f.write(data)

        self.stdout.write(self.style.SUCCESS(f'Successfully generated {output_path}'))

    def file(self):
        template_path = Path(settings.BASE_DIR) / 't-Dockerfile'
        with open(template_path, "r") as f:
            template_data = f.read()

        self.stdout.write(self.style.HTTP_INFO(f'Found template {template_path}'))

        config_data = pd.json_normalize(CONFIG.model_dump(), sep='_').to_dict(orient='records')[0]
        data = template_data.format(**config_data)

        output_path = Path(settings.BASE_DIR) / 'Dockerfile'
        with open(output_path, 'w') as f:
            f.write(data)

        self.stdout.write(self.style.SUCCESS(f'Successfully generated {output_path}'))

    def handle(self, *args, **options):
        self.compose()
        self.file()
