from django.contrib import admin

# Register your models here.

from .models import DocumentSource, Parish, ParishRef, Country, DocumentGroup, Province, County, Diocese, Deanery, ParishUser


class ParishUserInline(admin.TabularInline):
    model = ParishUser
    extra = 1


class ParishRefInline(admin.TabularInline):
    model = ParishRef
    extra = 1


class DocumentGroupInline(admin.TabularInline):
    model = DocumentGroup
    extra = 1


class DocumentSourceAdmin(admin.ModelAdmin):
    #fields = ('name', 'year', 'address')
    pass
admin.site.register(DocumentSource, DocumentSourceAdmin)


class DocumentGroupAdmin(admin.ModelAdmin):
    pass
admin.site.register(DocumentGroup, DocumentGroupAdmin)


class ParishAdmin(admin.ModelAdmin):
    list_display = ['name', 'year', 'country', 'province', 'county', 'place', 'address', 'geo_lat', 'geo_lng', 'diocese', 'deanery', 'access', ]
    list_filter = ['country', 'province', 'diocese', ]
    list_editable = ('access', )

    fieldsets = [
        (None, {'fields': ['name', 'year']}),
        ('Location', {'fields': ['country', 'province', 'county', 'place', 'address', 'geo_lat', 'geo_lng']}),
        ('Location2', {'fields': ['diocese', 'deanery']})
    ]

    inlines = [
        ParishUserInline, DocumentGroupInline
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