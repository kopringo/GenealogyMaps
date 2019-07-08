from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import *


###############################################################################
# import/export functions

class CourtOfficeResource(resources.ModelResource):
    class Meta:
        model = CourtOffice


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

class SourceAdmin(admin.ModelAdmin):
    list_display = ['name', 'short', 'group']
    list_filter = ['group', ]
    pass


class ParishAdmin(admin.ModelAdmin):
    list_display = ['name', 'year', 'province', 'county', 'place', 'geo_lat', 'geo_lng', 'diocese', 'deanery', 'access', ]
    list_filter = ['country', 'province', 'diocese', ]
    list_editable = ('access', )
    search_fields = ['name', 'place']

    fieldsets = [
        (None, {'fields': ['name', 'year', 'religion', ]}),
        ('Location', {'fields': ['country', 'province', 'county', 'place', 'address', 'geo_lat', 'geo_lng']}),
        ('Location2', {'fields': ['diocese', 'deanery']})
    ]

    inlines = [
        ParishSourceInline,
        #ParishUserInline
    ]


class ParishRefAdmin(admin.ModelAdmin):
    pass

class ParishUserAdmin(admin.ModelAdmin):
    pass

class ParishSourceExtAdmin(admin.ModelAdmin):
    pass


##########################################################

class CourtOfficeAdmin(ImportExportModelAdmin):
    list_display = ['name', 'ziemia_i_rp', ]
    list_filter = ['ziemia_i_rp', ]
    resource_class = CourtOfficeResource


class CourtBookAdmin(admin.ModelAdmin):
    list_display = ['name', 'office', ]
    list_filter = ['office', ]

class CourtBookSourceAdmin(ImportExportModelAdmin):
    list_display = ['book', 'source', 'copy_type', 'date_from', 'date_to']
    resource_class = CourtBookSourceResource

##########################################################

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




admin.site.register(Country, CountryAdmin)
admin.site.register(Province, ProvinceAdmin)
admin.site.register(County, CountyAdmin)
admin.site.register(Diocese, DioceseAdmin)
admin.site.register(Deanery, DeaneryAdmin)
admin.site.register(ZiemiaIRP, ZiemiaIRPAdmin)

admin.site.register(Parish, ParishAdmin)
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
