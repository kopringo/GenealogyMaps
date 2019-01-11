import json

from django.core.management.base import BaseCommand, CommandError
from GenealogyMaps.apps.core.models import Parish, Deanery, Diocese, Province, County, Country


class Command(BaseCommand):
    help = 'Import podstawowych danych "data"'

    #def add_arguments(self, parser):
    #    parser.add_argument('poll_id', nargs='+', type=int)

    def add_arguments(self, parser):
        parser.add_argument('-op', '--only-parishes', action='store_true', help='Import only parishes')

    def handle(self, *args, **options):

        only_selected = False
        only_parishes = options['only_parishes']
        if only_parishes:
            only_selected = True

        with open('data/initial_data2.json') as file:
            data = file.read()
            json_data = json.loads(data)

            country_pl = Country.objects.get(code='pl')

            if not only_selected:
                for provice_key in json_data['wojewodztwa']:
                    provice_raw = json_data['wojewodztwa'][provice_key]
                    #print(provice_raw)
                    province = Province()
                    province.pk = int(provice_raw['id'])
                    province.name = provice_raw['name']
                    province.country = country_pl
                    province.short = provice_raw['wojskrot']
                    try:
                        province.save()
                    except Exception as e:
                        self.stdout.write(self.style.ERROR('provice already exists'))

            if not only_selected:
                for county_key in json_data['powiaty']:
                    county_raw = json_data['powiaty'][county_key]
                    #print(county_raw)

                    try:
                        #print(county_raw['powskrot'])
                        province = Province.objects.get(short=county_raw['powskrot'])
                    except Exception as e:
                        self.stdout.write(self.style.ERROR('no province'))
                        continue

                    county = County()
                    county.pk = int(county_raw['id'])
                    county.name = county_raw['name']
                    county.province = province
                    try:
                        county.save()
                    except Exception as e:
                        self.stdout.write(self.style.ERROR('county already exists'))

            if not only_selected:
                for diecezja_id in json_data['diecezje']:
                    diecezja_raw = json_data['diecezje'][diecezja_id]

                    diocese = Diocese()
                    diocese.pk = int(diecezja_raw['id'])
                    diocese.name = diecezja_raw['name']
                    diocese.url = diecezja_raw['link']
                    diocese.country = country_pl
                    diocese.short = diecezja_raw['dieskrot']

                    try:
                        diocese.save()
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(e))

            if not only_selected:
                for dekanat_key in json_data['dekanaty']:
                    dekanat_raw = json_data['dekanaty'][dekanat_key]
                    #print(dekanat_raw)
                    #print(dekanat_raw['id'])
                    try:
                        diocese = Diocese.objects.get(short=dekanat_raw['dekskrot'])
                    except Exception as e:
                        self.stdout.write(self.style.ERROR('no diocese'))
                        continue

                    deanery = Deanery()
                    deanery.pk = int(dekanat_raw['id'])
                    deanery.name = dekanat_raw['name']
                    deanery.diocese = diocese

                    try:
                        deanery.save()
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(e))

            if not only_selected or only_parishes:
                for parafia in json_data['parafie']:

                    if not isinstance(parafia, dict):
                        self.stdout.write(self.style.ERROR('error with parish'))
                        continue
                    if 'name' not in parafia.keys():
                        self.stdout.write(self.style.ERROR('error with parish'))
                        continue

                    try:
                        province = Province.objects.get(pk=parafia['wojewodztwo_id'])
                        county = County.objects.get(pk=parafia['powiat_id'])
                        diocese = Diocese.objects.get(pk=parafia['diecezja_id'])
                    except Exception as e:
                        #self.stdout.write(e)
                        pass
                    try:
                        deanery = Deanery.objects.get(pk=parafia['dekanat_id'])
                    except:
                        deanery = None

                    #if not province:
                    #    print('no province')
                    #if not county:
                    #    print('no county')
                    #if not diocese:
                    #    print('no diocese')
                    #if not deanery:
                    #    print('no deanery')
                    #continue

                    parish = Parish()
                    parish.name = parafia['name']
                    parish.province = province
                    parish.county = county
                    parish.diocese = diocese
                    parish.deanery = deanery
                    try:
                        parish.gen_id = int(parafia['genealodzy_pid'])
                    except:
                        parish.gen_id = 0
                    try:
                        parish.geo_lat = parafia['lat']
                        parish.geo_lng = parafia['lng']
                    except:
                        pass

                    parish.year = 0
                    try:
                        parish.year = int(parafia['year'])
                    except:
                        pass
                    parish.place = parafia['location']
                    parish.address = parafia['address']
                    parish.postal_code = parafia['postal_code']
                    parish.postal_place = parafia['postal_place']

                    try:
                        parish.save()
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(e))



        self.stdout.write(self.style.SUCCESS('OK'))
