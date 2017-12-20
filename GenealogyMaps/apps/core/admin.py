from django.contrib import admin

# Register your models here.

from .models import Source, Parish, ParishRef

class SourceAdmin(admin.ModelAdmin):
    fields = ('name', 'year', 'address')
admin.site.register(Source, SourceAdmin)

class ParishAdmin(admin.ModelAdmin):
    pass
admin.site.register(Parish, ParishAdmin)

class ParishRefAdmin(admin.ModelAdmin):
    pass
admin.site.register(ParishRef, ParishRefAdmin)

