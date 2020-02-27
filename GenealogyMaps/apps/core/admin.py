from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field

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

    def before_import_row(self, row, **kwargs):
        #print('before_import_row' ,row, kwargs)


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
            row['dekanat'] = Deanery.objects.get(name__iexact=deanery)
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
            row['religion'] = int(row.get('wyznanie'))
        except:
            pass


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
        
        #widgets = {
        #        'published': {'format': '%d.%m.%Y'},
        #        }


class ParishSourceResource(resources.ModelResource):
    class Meta:
        model = ParishSource


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
        (None, {'fields': ['name', 'year', 'religion', ]}),
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
    list_filter = ['country', 'province', 'diocese', 'not_exist_anymore', ]
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

##########################################################


class CountryAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']


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
