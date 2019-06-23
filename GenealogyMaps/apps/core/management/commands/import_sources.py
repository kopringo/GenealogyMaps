import json

from django.core.management.base import BaseCommand, CommandError
from GenealogyMaps.apps.core.models import Parish, Deanery, Diocese, Province, County, Country,\
    Source


class Command(BaseCommand):
    help = 'Import podstawowych źródeł danych'

    def handle(self, *args, **options):

        sources = [

            # https://www.archiwa.gov.pl/pl/43-aktualnosci2
            {'id': 100, 'name': 'AP Białystok', 'url': 'http://www.bialystok.ap.gov.pl/', 'group': 'AP'},
            {'id': 101, 'name': 'AP Bydgoszcz', 'url': 'http://www.bydgoszcz.ap.gov.pl/', 'group': 'AP'},
            {'id': 102, 'name': 'AP Częstochowa', 'url': 'http://www.czestochowa.ap.gov.pl/', 'group': 'AP'},
            {'id': 103, 'name': 'AP Gdańsk', 'url': 'http://www.gdansk.ap.gov.pl/', 'group': 'AP'},
            {'id': 104, 'name': 'AP Gorzów Wielkopolski', 'url': 'http://www.gorzow.ap.gov.pl/', 'group': 'AP'},
            {'id': 105, 'name': 'AP Kalisz', 'url': 'http://www.archiwum.kalisz.pl/', 'group': 'AP'},
            {'id': 106, 'name': 'AP Katowice', 'url': 'http://www.katowice.ap.gov.pl/', 'group': 'AP'},
            {'id': 107, 'name': 'AP Kielce', 'url': 'http://www.kielce.ap.gov.pl/', 'group': 'AP'},
            {'id': 108, 'name': 'AP Koszalin', 'url': 'http://www.koszalin.ap.gov.pl/', 'group': 'AP'},
            {'id': 109, 'name': 'AP Kraków', 'url': 'http://www.archiwum.krakow.pl/', 'group': 'AP'},
            {'id': 110, 'name': 'AP Leszno', 'url': 'http://www.archiwum.leszno.pl/', 'group': 'AP'},
            {'id': 111, 'name': 'AP Lublin', 'url': 'http://www.lublin.ap.gov.pl/', 'group': 'AP'},
            {'id': 112, 'name': 'AP Łódź', 'url': 'http://www.lodz.ap.gov.pl/', 'group': 'AP'},
            {'id': 113, 'name': 'AP Malbork', 'url': 'http://www.malbork.ap.gov.pl/', 'group': 'AP'},
            {'id': 114, 'name': 'AP Olsztyn', 'url': 'http://www.olsztyn.ap.gov.pl/', 'group': 'AP'},
            {'id': 115, 'name': 'AP Opole', 'url': 'http://www.opole.ap.gov.pl/', 'group': 'AP'},
            {'id': 116, 'name': 'AP Piotrków Trybunalski', 'url': 'http://www.piotrkow-tryb.ap.gov.pl/', 'group': 'AP'},
            {'id': 117, 'name': 'AP Płock', 'url': 'http://www.plock.ap.gov.pl/', 'group': 'AP'},
            {'id': 118, 'name': 'AP Poznań', 'url': 'http://www.poznan.ap.gov.pl/', 'group': 'AP'},
            {'id': 119, 'name': 'AP Przemyśl', 'url': 'http://www.przemysl.ap.gov.pl/', 'group': 'AP'},
            {'id': 120, 'name': 'AP Radom', 'url': 'http://www.radom.ap.gov.pl/', 'group': 'AP'},
            {'id': 121, 'name': 'AP Rzeszów', 'url': 'http://www.rzeszow.ap.gov.pl/', 'group': 'AP'},
            {'id': 122, 'name': 'AP Siedlce', 'url': 'http://www.siedlce.ap.gov.pl/', 'group': 'AP'},
            {'id': 123, 'name': 'AP Suwałki', 'url': 'http://www.suwalki.ap.gov.pl/', 'group': 'AP'},
            {'id': 124, 'name': 'AP Szczecin', 'url': 'http://www.szczecin.ap.gov.pl/', 'group': 'AP'},
            {'id': 125, 'name': 'AP Toruń', 'url': 'http://www.torun.ap.gov.pl/', 'group': 'AP'},
            {'id': 126, 'name': 'AP Warszawa', 'url': 'http://warszawa.ap.gov.pl/', 'group': 'AP'},
            {'id': 127, 'name': 'AP Wrocław', 'url': 'http://www.ap.wroc.pl/', 'group': 'AP'},
            {'id': 128, 'name': 'AP Zamość', 'url': 'http://zamosc.ap.gov.pl/', 'group': 'AP'},
            {'id': 129, 'name': 'AP Zielona Góra', 'url': 'http://www.archiwum.zgora.pl/', 'group': 'AP'},

            {'id': 200, 'name': 'Archiwum Archidiecezjalne w Białymstoku', 'url': '', 'group': 'AD'},
            {'id': 201, 'name': 'Archiwum Archidiecezji Częstochowskiej', 'url': '', 'group': 'AD'},
            {'id': 202, 'name': 'Archiwum Diecezjalne w Drohiczynie', 'url': '', 'group': 'AD'},
            {'id': 203, 'name': 'Archiwum Diecezji Elbląskiej', 'url': '', 'group': 'AD'},
            {'id': 204, 'name': 'Archiwum Ełckiej Kurii Diecezjalnej', 'url': '', 'group': 'AD'},
            {'id': 205, 'name': 'Archiwum Archidiecezjalne w Gdańsku', 'url': '', 'group': 'AD'},
            {'id': 206, 'name': 'Archiwum Kurii Diecezjalnej w Gliwicach', 'url': '', 'group': 'AD'},
            {'id': 207, 'name': 'Archiwum Archidiecezjalne w Gnieźnie', 'url': '', 'group': 'AD'},
            {'id': 208, 'name': 'Archiwum Archidiecezjalne w Katowicach', 'url': '', 'group': 'AD'},
            {'id': 209, 'name': 'Archiwum Diecezjalne w Kielcach', 'url': '', 'group': 'AD'},
            {'id': 210, 'name': 'Archiwum Diecezji Koszalińsko-Kołobrzeskiej', 'url': '', 'group': 'AD'},
            {'id': 211, 'name': 'Archiwum Kurii Metropolitalnej w Krakowie', 'url': '', 'group': 'AD'},
            {'id': 212, 'name': 'Archiwum Arcybiskupa Eugeniusza Baziaka', 'url': '', 'group': 'AD'},
            {'id': 213, 'name': 'Archiwum Archidiecezjalne w Lublinie', 'url': '', 'group': 'AD'},
            {'id': 214, 'name': 'Archiwum Diecezjalne w Łomży', 'url': '', 'group': 'AD'},
            {'id': 215, 'name': 'Archiwum Archidiecezjalne w Łodzi', 'url': '', 'group': 'AD'},
            {'id': 216, 'name': 'Archiwum Diecezjalne w Opolu', 'url': '', 'group': 'AD'},
            {'id': 217, 'name': 'Archiwum Diecezjalne w Pelplinie', 'url': '', 'group': 'AD'},
            {'id': 218, 'name': 'Archiwum Diecezjalne Płockie', 'url': '', 'group': 'AD'},
            {'id': 219, 'name': 'Archiwum Archidiecezjalne w Poznaniu', 'url': '', 'group': 'AD'},
            {'id': 220, 'name': 'Archiwum Archidiecezjalne w Przemyślu', 'url': '', 'group': 'AD'},
            {'id': 221, 'name': 'Archiwum Diecezjalne w Sandomierzu', 'url': '', 'group': 'AD'},
            {'id': 222, 'name': 'Archiwum Diecezji Siedleckiej', 'url': '', 'group': 'AD'},
            {'id': 223, 'name': 'Archiwum Diecezjalne w Tarnowie', 'url': '', 'group': 'AD'},
            {'id': 224, 'name': 'Archiwum Akt Dawnych Diecezji Toruńskiej', 'url': '', 'group': 'AD'},
            {'id': 225, 'name': 'Archiwa Archidiecezjalne Warszawskie', 'url': '', 'group': 'AD'},
            {'id': 226, 'name': 'Archiwum Diecezjalne Warszawsko-Praskie', 'url': '', 'group': 'AD'},
            {'id': 227, 'name': 'Archiwum Diecezjalne we Włocławku', 'url': '', 'group': 'AD'},
            {'id': 228, 'name': 'Archiwum Archidiecezjalne we Wrocławiu', 'url': '', 'group': 'AD'},
            {'id': 229, 'name': 'Archiwum Diecezji Zamojsko-Lubaczowskiej', 'url': '', 'group': 'AD'},
            {'id': 230, 'name': 'Archiwum Diecezjalne w Zielonej Górze', 'url': '', 'group': 'AD'},
            
            {'id': 301, 'name': 'Archiwum Główne Akt Dawnych', 'url': 'http://www.agad.archiwa.gov.pl/', 'group': 'Other', 'short': 'AGAD'},
            {'id': 302, 'name': 'Archiwum Akt Nowych', 'url': 'http://aan.gov.pl/', 'group': 'Other', 'short': 'AAN'},
            {'id': 303, 'name': 'Narodowe Archiwum Cyfrowe', 'url': '', 'group': 'Other', 'short': 'NAC'},
            {'id': 304, 'name': 'Archiwum Parafialne', 'url': '', 'group': 'Other', 'short': ''},
            
        ]

        for source in sources:
            try:
                document_source = Source.objects.get(pk=source['id'])
            except Source.DoesNotExist:
                document_source = Source()
                document_source.id = source['id']

            document_source.name = source['name']
            document_source.url = source['url']
            document_source.group = source['group']
            try:
                document_source.save()
            except Exception as e:
                self.stdout.write(self.style.WARNING('error: %s' % str(e)))

        self.stdout.write(self.style.SUCCESS('OK'))
