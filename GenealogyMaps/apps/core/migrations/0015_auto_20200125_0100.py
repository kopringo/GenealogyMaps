# Generated by Django 2.2.2 on 2020-01-25 01:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_parish_century'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parish',
            name='century',
            field=models.CharField(blank=True, help_text='Wiek powstania', max_length=8, null=True),
        ),
    ]