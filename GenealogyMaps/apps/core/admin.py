from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

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
    name = Field(attribute='name', column_name='nazwa')
    wyznanie = Field(attribute='religion', column_name='wyznanie')
    year = Field(attribute='year', column_name='rok')
    century = Field(attribute='century', column_name='wiek')
    country = Field(attribute='country', column_name='kraj')
    province = Field(attribute='province', column_name='wojewodztwo')
    county = Field(attribute='county', column_name='powiat')
    diocese = Field(attribute='diocese', column_name='diecezja')
    deanery = Field(attribute='deanery', column_name='dekanat')
    place = Field(attribute='place', column_name='miejscowosc')
    #place2 = Field(attribute='place2', column_name='miejscowosc 2')

    def before_import_row(self, row, **kwargs):

        try:
            rok = row.get('rok')
            row['rok'] = int(rok)
        except:
            row['rok'] = 0

        try:
            country = row.get('kraj')
            row['kraj'] = Country.objects.get(code__iexact=country)
        except Exception as e:
            row['kraj'] = None #Country.objects.get(pk=1)

        try:
            province = row.get('wojewodztwo')
            row['wojewodztwo'] = Province.objects.get(name__iexact=province, country=row['kraj'])
        except Exception as e:
            row['wojewodztwo'] = None

        try:
            county = row.get('powiat')
            row['powiat'] = County.objects.get(name__iexact=county, province=row['wojewodztwo'])
        except Exception as e:
            row['powiat'] = '-'

        try:
            diocese = row.get('diecezja')
            row['diecezja'] = Diocese.objects.get(name__iexact=diocese, country=row['kraj'])
        except:
            row['diecezja'] = None

        try:
            deanery = row.get('dekanat')
            row['dekanat'] = Deanery.objects.get(name__iexact=deanery, diocese=row['diecezja'])
        except:
            row['dekanat'] = None

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

        try:
            wyznanie = row.get('wyznanie')
            wyznanie_id = wyznanie

            if wyznanie == 'grekokatolickie':
                wyznanie_id = 7
            if wyznanie == 'prawosławne':
                wyznanie_id = 6
            if wyznanie == 'ewangelicko-augsburskie':
                wyznanie_id = 5
            row['wyznanie'] = int(wyznanie_id)
        except:
            pass

        postal_code = row.get('postal_code', None)
        if postal_code is None:
            row['postal_code'] = ''
        postal_place = row.get('postal_place', None)
        if postal_place is None:
            row['postal_place'] = ''
        place2 = row.get('place2', None)
        if place2 is None:
            row['place2'] = ''
        nazwa = row.get('nazwa', None)
        if nazwa is None:
            row['nazwa'] = ''



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

    class Meta:
        model = Parish
        fields = (
            'id',
            'name', 'year', 'wyznanie', 
            'country', 'province', 'county', 'diocese', 'deanery',
            'place', 'postal_code', 'postal_place', 'address',
            'geo_lat', 'geo_lng', 'not_exist_anymore',
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
        #print(parish_source)
        if parish_source.parish:
            return '%s' % parish_source.parish.id
        return None

    def dehydrate_parish_name(self, parish_source):
        if parish_source.parish:
            return '%s' % parish_source.parish.name
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
            source = Source.objects.get(short=source_short)
            row['Źródło'] = source
        except:
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

        instance.parish = row.get('ID parafii')
        instance.type_b = row.get('type_b')
        instance.type_d = row.get('type_d')
        instance.type_m = row.get('type_m')
        instance.type_a = row.get('type_a')
        instance.type_zap = row.get('type_zap')

        return instance, new

#    def before_save_instance(self, instance, using_transactions, dry_run):
#        print(instance)

#    def after_import_row(self, row, row_result, **kwargs):
#        print('after_import_row', row, row_result)

#    def import_obj(self, obj, data, dry_run):
#        ret = super(ParishSourceResource, self).import_obj(obj, data, dry_run)
#        print('import_obj', obj, data)
#        print(obj.parish)
#        print('---')
#        return ret


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
    list_filter = ['country', 'province', 'diocese', 'not_exist_anymore', ]
    list_editable = ('access', )
    search_fields = ['name', 'place']

    fieldsets = [
        (None, {'fields': ['name', 'year', 'religion', 'visible', ]}),
        ('Location', {'fields': ['country', 'province', 'county', 'place', 'place2', 'address', 'geo_lat', 'geo_lng', 'not_exist_anymore']}),
        ('Location2', {'fields': ['diocese', 'deanery']}),
        ('Location3', {'fields': ['county_r1', 'county_r2', 'county_rz']}),
    ]

    inlines = [
        ParishSourceInline,
        #ParishUserInline
    ]
    
    resource_class = ParishResource


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
    fields = ['name', ]

class ProvinceInline(admin.TabularInline):
    model = Province
    extra = 1
    fields = ['name', ]

##########################################################


class CountryAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']

    inlines = [
        ProvinceInline
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
    list_filter = ['province', ]


class DioceseAdmin(admin.ModelAdmin):
    list_display = ['name', 'deanery_number', 'parish_number', 'public', ]
    list_editable = ('public', )


class DeaneryAdmin(admin.ModelAdmin):
    list_display = ['name', 'diocese']
    list_filter = ['diocese', ]


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
