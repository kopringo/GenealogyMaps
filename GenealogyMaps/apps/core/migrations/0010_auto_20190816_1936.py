# Generated by Django 2.2.3 on 2019-08-16 19:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20190805_1814'),
    ]

    operations = [
        migrations.AddField(
            model_name='courtoffice',
            name='address',
            field=models.CharField(blank=True, help_text='Adres, ulica i numer', max_length=32),
        ),
        migrations.AddField(
            model_name='courtoffice',
            name='county',
            field=models.ForeignKey(help_text='Powiat', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.County'),
        ),
        migrations.AddField(
            model_name='courtoffice',
            name='geo_lat',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='courtoffice',
            name='geo_lng',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='courtoffice',
            name='place',
            field=models.CharField(blank=True, help_text='Miejscowość', max_length=32),
        ),
        migrations.AddField(
            model_name='courtoffice',
            name='province',
            field=models.ForeignKey(help_text='Województwo', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.Province'),
        ),
        migrations.AddField(
            model_name='parish',
            name='main_parish',
            field=models.ForeignKey(blank=True, help_text='Parafia główna jeśli to jest filia', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='main_parish2', to='core.Parish'),
        ),
        migrations.AddField(
            model_name='parish',
            name='places',
            field=models.TextField(blank=True, help_text='Lista miejscowości'),
        ),
        migrations.AddField(
            model_name='source',
            name='address',
            field=models.CharField(blank=True, help_text='Adres, ulica i numer', max_length=32),
        ),
        migrations.AddField(
            model_name='source',
            name='country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.Country'),
        ),
        migrations.AddField(
            model_name='source',
            name='geo_lat',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='source',
            name='geo_lng',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='source',
            name='place',
            field=models.CharField(blank=True, help_text='Miejscowość', max_length=32),
        ),
    ]
