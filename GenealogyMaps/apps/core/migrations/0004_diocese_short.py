# Generated by Django 2.1.4 on 2018-12-23 01:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20181223_0109'),
    ]

    operations = [
        migrations.AddField(
            model_name='diocese',
            name='short',
            field=models.CharField(blank=True, max_length=3),
        ),
    ]