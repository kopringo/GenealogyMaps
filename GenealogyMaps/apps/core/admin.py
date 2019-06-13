from django.contrib import admin

# Register your models here.

from .models import DocumentSource, Parish, ParishRef, Country, Source, Province, County, Diocese, Deanery, \
    ParishUser, ZiemiaIRP, ParishRawData


class ParishUserInline(admin.TabularInline):
    model = ParishUser
    extra = 1


class ParishRefInline(admin.TabularInline):
    model = ParishRef
    extra = 1


class SourceInline(admin.TabularInline):
    model = Source
    extra = 1
    fields = ['source', 'type', 'type_b', 'type_d', 'type_m', 'type_a', 'date_from', 'date_to']
    readonly_fields = ('source', 'type', 'type_b', 'type_d', 'type_m', 'type_a', 'date_from', 'date_to')


class DocumentSourceAdmin(admin.ModelAdmin):
    #fields = ('name', 'year', 'address')
    pass


class SourceAdmin(admin.ModelAdmin):
    list_display = ['id_with_dates', 'parish', 'source', 'type', 'date_modified', 'user']


class ParishAdmin(admin.ModelAdmin):
    list_display = ['name', 'year', 'province', 'county', 'place', 'geo_lat', 'geo_lng', 'diocese', 'deanery', 'access', ]
    list_filter = ['country', 'province', 'diocese', ]
    list_editable = ('access', )
    search_fields = ['name', 'place']

    fieldsets = [
        (None, {'fields': ['name', 'year']}),
        ('Location', {'fields': ['country', 'province', 'county', 'place', 'address', 'geo_lat', 'geo_lng']}),
        ('Location2', {'fields': ['diocese', 'deanery']})
    ]

    inlines = [
        ParishUserInline, SourceInline
    ]


class ParishRefAdmin(admin.ModelAdmin):
    pass


class CountryAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']


class ProvinceAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'county_number', 'parish_number', 'public', ]
    list_editable = ('public', )

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


admin.site.register(DocumentSource, DocumentSourceAdmin)
admin.site.register(Source, SourceAdmin)
admin.site.register(Parish, ParishAdmin)
admin.site.register(ParishRef, ParishRefAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Province, ProvinceAdmin)
admin.site.register(County, CountyAdmin)
admin.site.register(Diocese, DioceseAdmin)
admin.site.register(Deanery, DeaneryAdmin)
admin.site.register(ZiemiaIRP, ZiemiaIRPAdmin)
admin.site.register(ParishRawData, ParishRawDataAdmin)