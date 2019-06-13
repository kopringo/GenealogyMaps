import json

from django.core.management.base import BaseCommand, CommandError
from GenealogyMaps.apps.core.models import Parish, Deanery, Diocese, Province, County, Country,\
    DocumentSource


class Command(BaseCommand):
    help = 'Import podstawowych źródeł danych'

    def handle(self, *args, **options):

        sources = [
            {'id': 1, 'name': 'Geneteka (indeksy)', 'url': 'https://geneteka.genealodzy.pl'},
            {'id': 2, 'name': 'Lubgens (indeksy)', 'url': 'https://lubgens.eu'},
            {'id': 3, 'name': 'Projekt Podlasie (indeksy)', 'url': 'https://projektpodlasie.pl'},
            {'id': 4, 'name': 'SZwA (zdjęcia)', 'url': 'https://szukajwarchiwach.pl'},
            {'id': 5, 'name': 'Family Search (zdjęcia)', 'url': 'https://www.familysearch.org'},
            {'id': 6, 'name': 'Archiwum Państwowe', 'url': ''},
            {'id': 7, 'name': 'Archiwum Diecezjalne', 'url': ''},
            {'id': 8, 'name': 'Inne miejsce', 'url': ''},
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
