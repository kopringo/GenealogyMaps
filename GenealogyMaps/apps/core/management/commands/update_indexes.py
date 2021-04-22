import json

import base64

import datetime
from django.utils import timezone
import requests
from django.db.models import Q
from django.core.management.base import BaseCommand, CommandError
from GenealogyMaps.apps.core.models import Parish, ParishIndexSource


class Command(BaseCommand):
    help = 'Aktualizuje informacje o indexach'

    def handle(self, *args, **options):

        objects_to_check = ParishIndexSource.objects.filter(Q(checked_date__lt=timezone.now() - datetime.timedelta(days=7))|Q(checked_date__isnull=True))
        for obj in objects_to_check:
            if obj.project == ParishIndexSource.PARISH_INDEX_SOURCE__PP:
                r = requests.get(obj.url)
                if r.status_code == 200:
                    text = r.text
                    start = text.find('[BEGIN INDEX TABLE]') + len('[BEGIN INDEX TABLE]') + 1
                    end = text.find('[END INDEX TABLE]')

                    try:
                        b64content = text[start:end]
                        obj.raw_data = base64.b64decode(b64content).decode('ascii')

                    except Exception as e:
                        print(e)
                    finally:
                        obj.checked_date = timezone.now()
                        obj.save()

        self.stdout.write(self.style.SUCCESS('OK'))
