import json

from django.core.management.base import BaseCommand, CommandError
from GenealogyMaps.apps.core.models import Parish, Deanery, Diocese, Province, County, Country

class Command(BaseCommand):
    help = 'Import podstawowych danych "data"'

    #def add_arguments(self, parser):
    #    parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):

        with open('data/initial_data.json') as file:
            data = file.read()
            json_data = json.loads(data)

            country_pl = Country.objects.get(code='pl')

            #print(json_data['wojewodztwa'])
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

            #print(json_data['powiaty'])
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


            #print(json_data['diecezje'])
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

            #print(json_data['dekanaty'])
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

            # parafie
            for parafia in json_data['parafie']:
                print(parafia['lat'])
                continue
                # {'diecezja_id': '25', 'dekanat_id': '474', 'wojewodztwo_id': '15', 'powiat_id': '262', 'location': 'Luboń',
                # 'year': '2012', 'old_lat': '0', 'old_lng': '0', 'address': 'ul. Źródlana', 'postal_code': '62-030',
                # 'postal_place': 'Luboń', 'phone1': '', 'phone2': '', 'parafia_b': '', 'parafia_m': '', 'parafia_d': '',
                # 'ad_b': '', 'ad_m': '', 'ad_d': '', 'genealodzy_pid': '10858', 'lat': 52.3501875, 'lng': 16.8780983}

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
                    self.stdout.write(self.style.ERROR(e))
                try:
                    deanery = Deanery.objects.get(pk=parafia['dekanat_id'])
                except:
                    deanery = None

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
