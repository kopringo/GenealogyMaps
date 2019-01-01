# Generated by Django 2.1.4 on 2018-12-22 23:42

from django.db import migrations

def create_countires(apps, schema_editor):
    Country = apps.get_model("core", "Country")
    Country.objects.bulk_create([
        Country(pk=1, code='pl', name="Polska"),
        Country(pk=2, code='ua', name="Ukraina"),
    ])

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_countires),
    ]