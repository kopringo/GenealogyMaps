import json

import base64
from abc import abstractmethod

import pandas as pd

import datetime
from django.utils import timezone
import requests
from django.db.models import Q, F
from django.core.management.base import BaseCommand, CommandError
from GenealogyMaps.apps.core.models import Parish, ParishIndexSource, RemoteSystems, RemoteSystemItem

class RemoteSystemDownloader:
    def __init__(self, rs_obj):
        self.rs_obj = rs_obj

    def execute(self):
        try:
            self._execute()
        except Exception as e:
            print(e)

        self.rs_obj.checked_date = timezone.now()
        self.rs_obj.save()

    def save_parish(self, parish_key, json_data):
        try:
            rsi = RemoteSystemItem.objects.get(system=self.rs_obj, key=parish_key)
        except RemoteSystemItem.DoesNotExist:
            rsi = RemoteSystemItem()
            rsi.key = parish_key
            rsi.system = self.rs_obj
        except Exception as e:
            print(e)
        rsi.raw_data = json_data
        rsi.save()

    @abstractmethod
    def _execute(self):
        raise NotImplemented()


class RS_WyszukiwarkaPHP(RemoteSystemDownloader):
    def _execute(self):
        r = requests.get('{}{}'.format(self.rs_obj.url, '/php/getdata.php?im=&naz=&miejsc=&rok1=&rok2=&inne=&malz=&naz_malz=&ojc=&mat=&naz_mat=&pag=1&sort1=2&sort2=1&sort3=0&metr=&dokl=000000000000&metod=1&rodz=1&zasob=1'))
        text = r.text
        table = pd.read_html(text)[0].to_dict(orient='index')
        for key in table.keys():
            row = table[key]
            parafia = row['USC/Parafia']
            self.save_parish(parafia, json.dumps({'b': row['Urodzenia'], 'm': row['Śluby'], 'd': row['Zgony']}))


class RS_Geneteka(RemoteSystemDownloader):
    def _execute(self):
        url = 'https://geneteka.genealodzy.pl/rejestry.php?lang=pol'
        r = requests.get(url)
        text = r.text
        table = pd.read_html(text)[0].to_dict()
        print(table)
        #TODO


class RS_Tgzc(RemoteSystemDownloader):
    def _execute(self):
        url = 'https://www.genealodzy.czestochowa.pl/indeksy_json.php'
        r = requests.get(url)
        # usuwam zbedne przecinki ktore przeszkadzaja parserowi jsona
        json_fixed = r.text.replace(' ', '').replace(',\n]', '\n]').replace(',\n}', '\n}')

        j = json.loads(json_fixed, strict=False)
        for key in j['indexes'].keys():
            self.save_parish(key, json.dumps({'b': j['indexes'][key]['birth'], 'm': j['indexes'][key]['marriage'], 'd': j['indexes'][key]['death']}))


class RS_Szwa(RemoteSystemDownloader):
    def _execute(self):
        pass


class RS_Lubgens(RemoteSystemDownloader):
    def _execute(self):
        url = 'https://regestry.lubgens.eu/viewpage.php?page_id=1053'
        r = requests.get(url, headers={'User-agent': 'Mozilla/5.0'})
        pos = r.text.find('Wybierz parafię na literę')
        text = r.text[pos:]

        for table_index in (0, 1):
            table = pd.read_html(text)[table_index].to_dict(orient='index')
            for key in table.keys():
                if table[key][0] == 'Nazwa parafii / miejscowości':
                    continue
                parafia = table[key][0]

                self.save_parish(parafia, {'b': table[key][1], 'm': table[key][3], 'd': table[key][5]})


class RS_Poznan(RemoteSystemDownloader):
    def _execute(self):
        pass


class RS_Basia(RemoteSystemDownloader):
    def _execute(self):
        url = 'http://basia.famula.pl/content-all.php?lang=pl'


class Command(BaseCommand):
    help = 'Aktualizuje informacje o zewnętrznych bazach'

    def handle(self, *args, **options):

        objects_to_check = RemoteSystems.objects.filter(Q(active=True)&(Q(check_date__lt=timezone.now() - datetime.timedelta(days=1))|Q(check_date__isnull=True)))
        for obj in objects_to_check:

            if obj.database_format == RemoteSystems.DATABASE_FORMAT__WYSZUKIWARKA_PHP:
                RS_WyszukiwarkaPHP(obj).execute()

            if obj.database_format == RemoteSystems.DATABASE_FORMAT__GENETEKA:
                RS_Geneteka(obj).execute()

            if obj.database_format == RemoteSystems.DATABASE_FORMAT__TGZC:
                RS_Tgzc(obj).execute()

            if obj.database_format == RemoteSystems.DATABASE_FORMAT__SZWA:
                RS_Szwa(obj).execute()

            if obj.database_format == RemoteSystems.DATABASE_FORMAT__LUBGENS:
                RS_Lubgens(obj).execute()

            if obj.database_format == RemoteSystems.DATABASE_FORMAT__POZNAN:
                RS_Poznan(obj).execute()

            if obj.database_format == RemoteSystems.DATABASE_FORMAT__BASIA:
                RS_Basia(obj).execute()

        self.stdout.write(self.style.SUCCESS('OK'))
