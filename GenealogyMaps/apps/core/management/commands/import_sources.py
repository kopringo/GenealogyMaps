import json

from django.core.management.base import BaseCommand, CommandError
from GenealogyMaps.apps.core.models import Parish, Deanery, Diocese, Province, County, Country,\
    DocumentSource


class Command(BaseCommand):
    help = 'Import podstawowych źródeł danych'

    def handle(self, *args, **options):

        sources = [
            {'id': 1, 'name': 'Archiwum Państwowe', 'url': ''},
            {'id': 2, 'name': 'Archiwum Diecezjalne', 'url': ''},
            {'id': 3, 'name': 'Archiwum Parafialne', 'url': ''},
            {'id': 99, 'name': 'Inne miejsce', 'url': ''},
        ]

        for source in sources:
            try:
                document_source = DocumentSource.objects.get(pk=source['id'])
            except DocumentSource.DoesNotExist:
                document_source = DocumentSource()
                document_source.id = source['id']

            document_source.name = source['name']
            document_source.url = source['url']
            try:
                document_source.save()
            except:
                self.stdout.write(self.style.WARNING('error'))

        self.stdout.write(self.style.SUCCESS('OK'))
