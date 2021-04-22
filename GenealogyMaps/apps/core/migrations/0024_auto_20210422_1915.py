# Generated by Django 2.2.18 on 2021-04-22 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_auto_20210421_1116'),
    ]

    operations = [
        migrations.AddField(
            model_name='parishplace',
            name='existing',
            field=models.BooleanField(default=True, help_text='Obiekt istniejący'),
        ),
        migrations.AddField(
            model_name='parishplace',
            name='type',
            field=models.IntegerField(choices=[(0, 'Inny'), (1, 'Cmentarz')], default=1),
        ),
        migrations.AlterField(
            model_name='parishindexsource',
            name='project',
            field=models.IntegerField(choices=[(0, 'Test'), (1, 'Projekt Podlasie')], default=0),
        ),
        migrations.AlterField(
            model_name='parishplace',
            name='name',
            field=models.CharField(help_text='Opis', max_length=32),
        ),
        migrations.AlterField(
            model_name='source',
            name='group',
            field=models.CharField(blank=True, choices=[('AP', 'Archiwa Państwowe (PL)'), ('AD', 'Archiwa Kościelne (PL)'), ('PAR', 'Archiwum Parafialne (ALL)'), ('A_Z', 'Archiwa Zagraniczne'), ('Other', 'Inne')], default='Other', help_text='Grupa źródeł', max_length=32),
        ),
    ]