# Generated by Django 2.2.2 on 2020-03-08 00:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_auto_20200125_0116'),
    ]

    operations = [
        migrations.CreateModel(
            name='ParishLocations',
            fields=[
            ],
            options={
                'verbose_name': 'Parafia - lokalizacja',
                'verbose_name_plural': 'Parafie - lokalizacje',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('core.parish',),
        ),
        migrations.AlterModelOptions(
            name='county',
            options={'ordering': ['name'], 'verbose_name': 'Powiat', 'verbose_name_plural': 'Region - Powiaty'},
        ),
        migrations.AlterModelOptions(
            name='province',
            options={'ordering': ['name'], 'verbose_name': 'Województwo', 'verbose_name_plural': 'Region - Województwa'},
        ),
        migrations.AddField(
            model_name='parish',
            name='slug',
            field=models.CharField(help_text='Unikatowy losowy identyfikator parafii', max_length=16, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='parishsource',
            name='meta_record',
            field=models.BooleanField(default=False, help_text='Meta rekord oznacza serię ksiąg parafialnych w podanym zakresie'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='lastnames',
            field=models.TextField(blank=True, help_text='Nazwiska ktorymi interesuje sie uzytkownik'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='parishes',
            field=models.TextField(blank=True, help_text='Parafie ktorymi interesuje sie uzytkownik'),
        ),
        migrations.AlterField(
            model_name='courtbooksource',
            name='copy_type',
            field=models.IntegerField(choices=[(None, ''), (6, 'Księga'), (4, 'Sumariusz'), (7, 'Reptularz'), (99, '-------------------'), (1, 'Oryginał'), (2, 'Duplikat ASC / USC'), (3, 'Odpis'), (5, 'Kopia dekanalna')], default=None),
        ),
        migrations.AlterField(
            model_name='parishsource',
            name='copy_type',
            field=models.IntegerField(choices=[(None, ''), (6, 'Księga'), (4, 'Sumariusz'), (7, 'Reptularz'), (99, '-------------------'), (1, 'Oryginał'), (2, 'Duplikat ASC / USC'), (3, 'Odpis'), (5, 'Kopia dekanalna')], default=None),
        ),
    ]