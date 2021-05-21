from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.db.models import Q

from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field
from import_export import widgets

from .models import *


###############################################################################
# import/export functions

class CourtOfficeResource(resources.ModelResource):
    class Meta:
        model = CourtOffice


class ParishResource(resources.ModelResource):

    # obligatoryjne
    name = Field(attribute='name', column_name='nazwa')
    place = Field(attribute='place', column_name='miejscowosc')
    religion = Field(attribute='religion', column_name='wyznanie')

    country = Field(attribute='country', column_name='kraj r3')
    province = Field(attribute='province', column_name='wojewodztwo r3')
    county = Field(attribute='county', column_name='powiat r3')

    # opcjonalne
    year = Field(attribute='year', column_name='rok')
    century = Field(attribute='century', column_name='wiek')
    diocese = Field(attribute='diocese', column_name='diecezja r3')
    deanery = Field(attribute='deanery', column_name='dekanat r3')

    #postal_code = Field(attribute='postal_code', column_name='postal_code')
    #postal_place = Field(attribute='postal_place', column_name='postal_place')
    #address = Field(attribute='address', column_name='address')

    county_r1 = Field(attribute='county_r1', column_name='powiat r1')
    county_r2 = Field(attribute='county_r2', column_name='powiat r2')
    county_rz = Field(attribute='county_rz', column_name='powiat rz')
    deanery_r1 = Field(attribute='deanery_r1', column_name='dekanat r1')
    deanery_r2 = Field(attribute='deanery_r2', column_name='dekanat r2')
    deanery_rz = Field(attribute='deanery_rz', column_name='dekanat rz')

    # geo_lat
    # geo_lng
    # geo_validated
    # not_exist_anymore

    def before_import_row(self, row, **kwargs):

        try:
            rok = row.get('rok')
            row['rok'] = int(rok)
        except:
            row['rok'] = 0

        try:
            wyznanie = row.get('wyznanie')
            wyznanie_id = wyznanie

            if wyznanie == 'grekokatolickie':
                wyznanie_id = 7
            if wyznanie == 'prawosławne':
                wyznanie_id = 6
            if wyznanie == 'ewangelicko-augsburskie':
                wyznanie_id = 5
            if wyznanie.upper() in RELIGION_TYPE_SHORT.values():
                inverted_RELIGION_TYPE_SHORT = {value: key for key, value in RELIGION_TYPE_SHORT.items()}
                wyznanie_id = inverted_RELIGION_TYPE_SHORT[wyznanie.upper()]
            row['wyznanie'] = int(wyznanie_id)
        except Exception as e:
            print(e)
            pass

        try:
            country = row.get('kraj r3')
            row['kraj r3'] = Country.objects.get(Q(Q(code__iexact=country)|Q(name__iexact=country))&Q(historical_period=3))
        except Exception as e:
            row['kraj r3'] = None #Country.objects.get(pk=1)

        try:
            province = row.get('wojewodztwo r3')
            row['wojewodztwo r3'] = Province.objects.get(name__iexact=province, country__historical_period=3)
        except Exception as e:
            row['wojewodztwo r3'] = None

        try:
            diocese = row.get('diecezja r3')
            row['diecezja r3'] = Diocese.objects.get(name__iexact=diocese, country__historical_period=3)
        except:
            row['diecezja r3'] = None

#        try:
#            deanery = row.get('dekanat r3')
#            row['dekanat r3'] = Deanery.objects.get(name__iexact=deanery, diocese__country__historical_period=3)
#        except Except as e:
#            print(e)
#            row['dekanat r3'] = None

        for obj in [('powiat r2', 2), ('powiat r1', 1), ('powiat rz', 4), ('powiat r3', 3)]:
            try:
                county = row.get(obj[0])
                row[obj[0]] = County.objects.get(name__iexact=county, province__country__historical_period=obj[1])
            except Exception as e:
                print(e)
                row[obj[0]] = None

        for obj in [('dekanat r2', 2), ('dekanat r1', 1), ('dekanat rz', 4), ('dekanat r3', 3)]:
            try:
                deanery = row.get(obj[0])
                row[obj[0]] = Deanery.objects.get(name__iexact=deanery, diocese__country__historical_period=obj[1])
            except Exception as e:
                row[obj[0]] = None


        try:
            geo_lat = row.get('geo_lat')
            row['geo_lat'] = geo_lat.replace(',', '.')
        except:
            pass
        try:
            geo_lng = row.get('geo_lng')
            row['geo_lng'] = geo_lng.replace(',', '.')
        except:
            pass



        # pola ktore moga byc puste nie moga byc nullami
        for field in ['postal_code', 'postal_place', 'place2', 'nazwa', 'wiek', ]:
            val = row.get(field, None)
            if val is None:
                row[field] = ''


    def dehydrate_religion(self, parish):
        if parish.religion in RELIGION_TYPE_SHORT.keys():
            return RELIGION_TYPE_SHORT[parish.religion]
        return parish.religion

    def dehydrate_country(self, parish):
        if parish.country is not None:
            return '%s' % parish.country.code
        return ''

    def dehydrate_province(self, parish):
        if parish.province is not None:
            return '%s' % parish.province.name
        return ''

    def dehydrate_county(self, parish):
        try:
            if parish.county is not None:
                return '%s' % parish.county.name
        except:
            dir(parish)
        return ''



    def dehydrate_diocese(self, parish):
        if parish.diocese is not None:
            return '%s' % parish.diocese.name
        return ''

    def dehydrate_deanery(self, parish):
        if parish.deanery is not None:
            return '%s' % parish.deanery.name
        return ''

    def dehydrate_county_r1(self, parish):
        if parish.county_r1 is not None:
            return '%s' % parish.county_r1.name
        return ''

    def dehydrate_county_r2(self, parish):
        if parish.county_r2 is not None:
            return '%s' % parish.county_r2.name
        return ''

    def dehydrate_county_rz(self, parish):
        if parish.county_rz is not None:
            return '%s' % parish.county_rz.name
        return ''

    def dehydrate_deanery_r1(self, parish):
        if parish.deanery_r1 is not None:
            return '%s' % parish.deanery_r1.name
        return ''

    def dehydrate_deanery_r2(self, parish):
        if parish.deanery_r2 is not None:
            return '%s' % parish.deanery_r2.name
        return ''

    def dehydrate_deanery_rz(self, parish):
        if parish.deanery_rz is not None:
            return '%s' % parish.deanery_rz.name
        return ''

    class Meta:
        model = Parish
        fields = (

            'id',
            'name', 'religion', 'country', 'province', 'county', 'place',

            'year', 'century', 'diocese', 'deanery', 'postal_code', 'postal_place', 'address',
            'county_r1', 'county_r2', 'county_rz', 'deanery_r1', 'deanery_r2', 'deanery_rz', 'geo_lat', 'geo_lng',
            'geo_validated', 'not_exist_anymore'

            )
        export_order = fields


class ParishSourceResource(resources.ModelResource):

    parish = Field(attribute='parish', column_name='ID parafii')
    parish_name = Field(column_name='Nazwa parafii')
    source = Field(attribute='source', column_name='Źródło')
    copy_type = Field(attribute='copy_type', column_name='Typ dokumentu')
    date_from = Field(attribute='date_from', column_name='Lata od')
    date_to = Field(attribute='date_to', column_name='Lata do')
    meta_record = Field(attribute='meta_record', column_name='Meta roczniki')
    type = Field(column_name='Rodzaj akt')
    note = Field(attribute='note', column_name='Notatka')

    def dehydrate_parish(self, parish_source):
        try:
            if parish_source.parish:
                return '%s' % parish_source.parish.id
        except:
            pass
        return None

    def dehydrate_parish_name(self, parish_source):
        try:
            if parish_source.parish:
                return '%s' % parish_source.parish.name
        except:
            pass
        return None

    def dehydrate_type(self, parish_source):
        types = []
        if parish_source.type_b:
            types.append('B')
        if parish_source.type_d:
            types.append('D')
        if parish_source.type_m:
            types.append('M')
        if parish_source.type_a:
            types.append('A')
        if parish_source.type_zap:
            types.append('ZAP')

        return ' '.join(types)

    def dehydrate_copy_type(self, parish_source):
        return parish_source.copy_type_str()

    def dehydrate_meta_record(self, parish_source):
        if parish_source.meta_record:
            return 'Tak'
        return ''

    def before_import_row(self, row, **kwargs):

        parish_id = row.get('ID parafii')
        try:
            parish = Parish.objects.get(pk=parish_id)

            row['ID parafii'] = parish
        except Exception as e:
            row['ID parafii'] = '<brak parafi o id: %s>' % str(parish_id)

        source_short = row.get('Źródło')
        try:
            if 'Archiwum Parafialne'.lower() == source_short.lower().strip() or \
               'Archiwum Parafii'.lower() == source_short.lower().strip():
                source = Source.objects.get(a_par_for_auto_import=True)

            else:
                source = Source.objects.get(short=source_short)
            row['Źródło'] = source
        except Exception as e:
            print(str(e))
            row['Źródło'] = '<bledna nazwa zrodla: %s>' % source_short

        try:
            copy_type = str(row.get('Typ dokumentu')).lower()

            copy_type_id = SourceRef.str_to_copy_type(copy_type)
            if copy_type_id is None:
                copy_type_id = 6

            row['copy_type'] = copy_type_id
            row['Typ dokumentu'] = copy_type_id
        except Exception as e:
            print(str(e))

        try:
            rodzaj = str(row.get('Rodzaj akt')).strip().upper()
            _rodzaje = rodzaj.split(' ')

            for row_type in ['type_b', 'type_d', 'type_m', 'type_a', 'type_zap']:
                row[row_type] = False

            for _rodzaj in _rodzaje:

                if _rodzaj == 'B':
                    row['type_b'] = True
                if _rodzaj == 'D':
                    row['type_d'] = True
                if _rodzaj == 'M':
                    row['type_m'] = True
                if _rodzaj == 'A':
                    row['type_a'] = True
                if _rodzaj == 'ZAP':
                    row['type_zap'] = True
        except Exception as e:
            print(str(e))

        meta_r = row.get('Meta roczniki')
        if meta_r is not None:
            row['Meta roczniki'] = True
        else:
            row['Meta roczniki'] = False

        note = row.get('Notatka')
        if note is None:
            note = ''
        row['Notatka'] = note


    def get_or_init_instance(self, instance_loader, row):
        instance, new = super(ParishSourceResource, self).get_or_init_instance(instance_loader, row)

        #instance.parish = row.get('ID parafii')
        instance.type_b = row.get('type_b')
        instance.type_d = row.get('type_d')
        instance.type_m = row.get('type_m')
        instance.type_a = row.get('type_a')
        instance.type_zap = row.get('type_zap')

        return instance, new

    def after_save_instance(self, instance, using_transactions, dry_run):
        try:
            instance.parish.partial_done = True
            instance.parish.save()
        except Exception as e:
            print(str(e))


    class Meta:
        model = ParishSource
        fields = (
            'id', 'parish', 'parish_name', 'source', 'copy_type', 'type', 'date_from', 'date_to', 'note', 'meta_record'
        )
        #exclude = ('type_b', )
        export_order = fields


class CourtBookSourceResource(resources.ModelResource):
    class Meta:
        model = CourtBookSource

###############################################################################


class ParishUserInline(admin.TabularInline):
    model = ParishUser
    extra = 1


class SourceInline(admin.TabularInline):
    model = Source
    extra = 1
    #fields = ['source', 'type_b', 'type_d', 'type_m', 'type_a', 'date_from', 'date_to']
    #readonly_fields = ('source', 'type_b', 'type_d', 'type_m', 'type_a', 'date_from', 'date_to')


class ParishSourceAdmin(ImportExportModelAdmin):
    list_display = ['parish', 'source', 'type_b', 'type_m', 'type_d', 'type_a', 'type_sum_only', 'date_from', 'date_to']
    fieldsets = [
        (None, {'fields': ['parish', 'source', 'copy_type', 'note']}),
        ('Details', {'fields': ['type_b', 'type_m', 'type_d', 'type_a', 'type_sum_only', 'date_from', 'date_to']}),
        ('Creator', {'fields': ['user', 'date_created', 'date_modified']})
    ]
    resource_class = ParishSourceResource


class ParishSourceInline(admin.TabularInline):
    model = ParishSource
    extra = 0
    fields = ['source', 'copy_type', 'type_b', 'type_m', 'type_d', 'type_a', 'type_sum_only', 'date_from', 'date_to', 'user', 'date_modified']
    readonly_fields = ('source', 'user', 'date_modified')
    fk_name = 'parish'


class SourceAdmin(admin.ModelAdmin):
    list_display = ['name', 'short', 'group']
    list_filter = ['group', ]
    pass


class ParishAdmin(ImportExportModelAdmin):
    list_display = ['name', 'year', 'province', 'county', 'place', 'geo_lat', 'geo_lng', 'diocese', 'deanery', 'access', ]
    list_filter = ['country', 'province', 'diocese', 'not_exist_anymore', 'all_done', 'partial_done']
    list_editable = ('access', )
    search_fields = ['name', 'place']

    fieldsets = [
        (None, {'fields': ['name', 'year', 'religion', 'visible', ]}),
        ('Location', {'fields': ['country', 'place', 'place2', 'address', 'geo_lat', 'geo_lng', 'not_exist_anymore']}),
        ('Lokalizacja współczesna', {'fields': ['province', 'county', 'diocese', 'deanery']}),
        ('Lokalizacje historyczne świeckie', {'fields': ['county_r1', 'county_r2', 'county_rz']}),
        ('Lokalizacje historyczne kościelne', {'fields': ['deanery_r1', 'deanery_r2', 'deanery_rz']}),

    ]

    inlines = [
        ParishSourceInline,
        #ParishUserInline
    ]
    
    resource_class = ParishResource


class ParishIndexSourceAdmin(admin.ModelAdmin):
    pass



class ParishLocationsAdmin(admin.ModelAdmin):
    list_display = ['name', 'place', 'year', 'diocese', 'country', 'province', 'county', 'county_r2', 'county_r1', 'county_rz' ]
    list_filter = [ 'diocese', 'not_exist_anymore', ]
    list_editable = ('country', 'province', 'county', 'county_r2', 'county_r1', 'county_rz', )
    search_fields = ['name', 'place']
    list_per_page = 20


class ParishRefAdmin(admin.ModelAdmin):
    pass


class ParishUserAdmin(admin.ModelAdmin):
    list_display = ['parish', 'user', 'favorite', 'manager', ]
    list_filter = ['favorite', 'manager']


class ParishSourceExtAdmin(admin.ModelAdmin):
    pass


##########################################################

class CourtOfficeAdmin(ImportExportModelAdmin):
    list_display = ['name', 'ziemia_i_rp', ]
    list_filter = ['ziemia_i_rp', ]
    resource_class = CourtOfficeResource


class CourtBookAdmin(admin.ModelAdmin):
    list_display = ['name', 'office', 'owner', ]
    list_filter = ['office', ]


class CourtBookSourceAdmin(ImportExportModelAdmin):
    list_display = ['book', 'source', 'copy_type', 'date_from', 'date_to']
    resource_class = CourtBookSourceResource

##########################################################


class CountyInline(admin.TabularInline):
    model = County
    extra = 1
    show_change_link = True
    fields = ['name', ]


class ProvinceInline(admin.TabularInline):
    model = Province
    extra = 1
    show_change_link = True
    fields = ['name', 'public', ]


class DioceseInline(admin.TabularInline):
    model = Diocese
    extra = 1
    show_change_link = True
    fields = ['name', 'public', ]


class DeaneryInline(admin.TabularInline):
    model = Deanery
    extra = 1
    show_change_link = True
    fields = ['name', ]

##########################################################


class CountryAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'public', 'historical_period']
    list_filter = ['public', 'historical_period']

    inlines = [
        ProvinceInline,
        DioceseInline
    ]


class ProvinceAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'county_number', 'parish_number', 'public', ]
    list_editable = ('public', )
    list_filter = ['country', 'public', ]

    inlines = [
        CountyInline
    ]


class CountyAdmin(admin.ModelAdmin):
    list_display = ['name', 'province', 'parish_number', ]
    list_filter = ['province__country', ]


class DioceseAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'deanery_number', 'parish_number', 'public', 'religion', ]
    list_editable = ('public', 'religion', )
    list_filter = ['country', 'public', 'religion', ]

    inlines = [
        DeaneryInline
    ]


class DeaneryAdmin(admin.ModelAdmin):
    list_display = ['name', 'diocese']
    list_filter = ['diocese', ]


##########################################################


class ZiemiaIRPAdmin(admin.ModelAdmin):
    list_display = ['name',]


class ParishRawDataAdmin(admin.ModelAdmin):
    list_display = ['data_source', 'data_key', 'parish', ]
    list_filter = ['data_source', ]


admin.site.register(Country, CountryAdmin)
admin.site.register(Province, ProvinceAdmin)
admin.site.register(County, CountyAdmin)
admin.site.register(Diocese, DioceseAdmin)
admin.site.register(Deanery, DeaneryAdmin)
admin.site.register(ZiemiaIRP, ZiemiaIRPAdmin)

admin.site.register(Parish, ParishAdmin)
admin.site.register(ParishLocations, ParishLocationsAdmin)
admin.site.register(ParishSource, ParishSourceAdmin)
admin.site.register(ParishUser, ParishUserAdmin)
admin.site.register(ParishSourceExt, ParishSourceExtAdmin)
admin.site.register(ParishIndexSource, ParishIndexSourceAdmin)

admin.site.register(CourtOffice, CourtOfficeAdmin)
admin.site.register(CourtBook, CourtBookAdmin)
admin.site.register(CourtBookSource, CourtBookSourceAdmin)

admin.site.register(Source, SourceAdmin)

# user profile

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

"""
class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
"""
