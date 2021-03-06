# Generated by Django 2.2.3 on 2019-07-20 15:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20190708_1224'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='public',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='parish',
            name='all_done',
            field=models.BooleanField(default=False, help_text='Oznacza parafię całkowicie uzuepłnioną\xa0(wg wiedzy opiekunów)'),
        ),
        migrations.AddField(
            model_name='parish',
            name='not_exist_anymore',
            field=models.BooleanField(default=False, help_text='Parafia już nie istnieje'),
        ),
        migrations.AlterField(
            model_name='courtbooksource',
            name='copy_type',
            field=models.IntegerField(choices=[(1, 'Oryginał'), (2, 'Duplikat ASC / USC'), (5, 'Kopia dekanalna'), (4, 'Sumariusz')], default=1),
        ),
        migrations.AlterField(
            model_name='parish',
            name='deanery',
            field=models.ForeignKey(blank=True, help_text='Dekanat', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.Deanery'),
        ),
        migrations.AlterField(
            model_name='parish',
            name='diocese',
            field=models.ForeignKey(blank=True, help_text='Diecezja', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.Diocese'),
        ),
        migrations.AlterField(
            model_name='parish',
            name='gen_id',
            field=models.IntegerField(blank=True, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='parish',
            name='geo_lat',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='parish',
            name='geo_lng',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='parish',
            name='province',
            field=models.ForeignKey(help_text='Województwo', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.Province'),
        ),
        migrations.AlterField(
            model_name='parish',
            name='year',
            field=models.IntegerField(blank=True, help_text='Data erygowania', null=True),
        ),
        migrations.AlterField(
            model_name='parishsource',
            name='copy_type',
            field=models.IntegerField(choices=[(1, 'Oryginał'), (2, 'Duplikat ASC / USC'), (5, 'Kopia dekanalna'), (4, 'Sumariusz')], default=1),
        ),
    ]
