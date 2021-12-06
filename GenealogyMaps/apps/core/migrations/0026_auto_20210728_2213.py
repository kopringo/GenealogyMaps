# Generated by Django 2.2.18 on 2021-07-28 22:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_auto_20210512_0656'),
    ]

    operations = [
        migrations.AddField(
            model_name='parish',
            name='has_indexes',
            field=models.BooleanField(default=False, help_text='Flaga oznacza, że parafia ma dodane zewnętrzne indexy'),
        ),
        migrations.AlterField(
            model_name='parish',
            name='county',
            field=models.ForeignKey(blank=True, help_text='Powiat (R3)', limit_choices_to=models.Q(province__country__historical_period=3), null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.County'),
        ),
        migrations.AlterField(
            model_name='parish',
            name='postal_code',
            field=models.CharField(blank=True, help_text='Kod pocztowy', max_length=16),
        ),
        migrations.AlterField(
            model_name='parish',
            name='postal_place',
            field=models.CharField(blank=True, help_text='Poczta', max_length=32),
        ),
        migrations.AlterField(
            model_name='parish',
            name='province',
            field=models.ForeignKey(blank=True, help_text='Województwo (R3)', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.Province'),
        ),
    ]