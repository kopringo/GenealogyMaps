import json

from django.core.management.base import BaseCommand, CommandError
from GenealogyMaps.apps.core.models import ParishSource, Parish


class Command(BaseCommand):
    help = 'Ustawia flage partial_done dla parafii ktore maja min 1 ksiege'

    def handle(self, *args, **options):

        parish_list = ParishSource.objects.values('parish').distinct()
        for row in parish_list:
            try:
                parish = Parish.objects.get(pk=row['parish'])
                parish.partial_done = True
                parish.save()
            except:
                self.stdout.write(self.style.ERROR('no parish: %s' % str(row['parish'])))

        self.stdout.write(self.style.SUCCESS('OK'))
