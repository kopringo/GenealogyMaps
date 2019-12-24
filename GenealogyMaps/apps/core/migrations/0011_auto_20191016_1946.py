# Generated by Django 2.2.2 on 2019-10-16 19:46

import GenealogyMaps.apps.core.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20190816_1936'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='historical_period',
            field=models.IntegerField(choices=[(1, 'I RP'), (2, 'II RP'), (3, 'III RP')], default=1, help_text='Okres historyczny'),
        ),
        migrations.AddField(
            model_name='parish',
            name='county_r1',
            field=models.ForeignKey(help_text='Powiat (R1)', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='county_r1', to='core.County'),
        ),
        migrations.AddField(
            model_name='parish',
            name='county_r2',
            field=models.ForeignKey(help_text='Powiat (R2)', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='county_r2', to='core.County'),
        ),
        migrations.AddField(
            model_name='parish',
            name='county_rz',
            field=models.ForeignKey(help_text='Powiat (RZ)', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='county_rz', to='core.County'),
        ),
        migrations.AddField(
            model_name='parish',
            name='year_inexact',
            field=models.BooleanField(default=False, help_text='Czy data niedokładna'),
        ),
        migrations.AlterField(
            model_name='parish',
            name='county',
            field=models.ForeignKey(help_text='Powiat (R3)', on_delete=django.db.models.deletion.DO_NOTHING, to='core.County'),
        ),
        migrations.AlterField(
            model_name='parish',
            name='province',
            field=models.ForeignKey(help_text='Województwo (R3)', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.Province'),
        ),
        migrations.AlterField(
            model_name='parish',
            name='year',
            field=models.IntegerField(blank=True, help_text='Data erygowania', null=True, validators=[GenealogyMaps.apps.core.models.my_year_validator]),
        ),
        migrations.AlterField(
            model_name='parishsource',
            name='date_from',
            field=models.IntegerField(default=1800, help_text='Zakres dat: od roku', validators=[GenealogyMaps.apps.core.models.my_year_validator]),
        ),
        migrations.AlterField(
            model_name='parishsource',
            name='date_to',
            field=models.IntegerField(default=1900, help_text='Zakres dat: do roku', validators=[GenealogyMaps.apps.core.models.my_year_validator]),
        ),
        migrations.AlterField(
            model_name='source',
            name='group',
            field=models.CharField(blank=True, choices=[('AP', 'Archiwa Państwowe (PL)'), ('AD', 'Archiwa Kościelne (PL)'), ('PAR', 'Archiwum Parafialne'), ('BIB', 'Biblioteki'), ('USC', 'Urzędy Stanu Cywilnego'), ('Other', 'Inne')], default='Other', help_text='Grupa źródeł', max_length=32),
        ),
    ]
