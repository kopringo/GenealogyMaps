from django.contrib import admin

# Register your models here.

from .models import DocumentSource, Parish, ParishRef, Country, DocumentGroup, Province, County, Diocese, Deanery

class DocumentSourceAdmin(admin.ModelAdmin):
    fields = ('name', 'year', 'address')
admin.site.register(DocumentSource, DocumentSourceAdmin)

class DocumentGroupAdmin(admin.ModelAdmin):
    pass
admin.site.register(DocumentGroup, DocumentGroupAdmin)

class ParishAdmin(admin.ModelAdmin):
    list_display = ['name', 'year', 'country', 'province', 'county', 'place', 'address', 'geo_lat', 'geo_lng', 'diocese', 'deanery', ]
    list_filter = ['country', 'province', 'diocese', ]

    fieldsets = [
        (None, {'fields': ['name', 'year']}),
        ('Location', {'fields': ['country', 'province', 'county', 'place', 'address', 'geo_lat', 'geo_lng']}),
        ('Location2', {'fields': ['diocese', 'deanery']})
    ]
admin.site.register(Parish, ParishAdmin)

class ParishRefAdmin(admin.ModelAdmin):
    pass
admin.site.register(ParishRef, ParishRefAdmin)

class CountryAdmin(admin.ModelAdmin):
    pass
admin.site.register(Country, CountryAdmin)

class ProvinceAdmin(admin.ModelAdmin):
    pass
admin.site.register(Province, ProvinceAdmin)

class CountyAdmin(admin.ModelAdmin):
    pass
admin.site.register(County, CountyAdmin)

class DioceseAdmin(admin.ModelAdmin):
    pass
admin.site.register(Diocese, DioceseAdmin)

class DeaneryAdmin(admin.ModelAdmin):
    pass
admin.site.register(Deanery, DeaneryAdmin)