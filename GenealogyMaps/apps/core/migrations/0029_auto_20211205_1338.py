# Generated by Django 2.2.18 on 2021-12-05 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_remotesystems_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='remotesystems',
            name='database_format',
            field=models.IntegerField(choices=[(0, 'Test'), (1, 'Wyszukiwarka PHP by MB'), (2, 'Geneteka (@TODO)'), (3, 'TGZC'), (4, 'SZwA (@TODO)'), (5, 'Lubgens'), (6, 'Poznan'), (7, 'Basia')]),
        ),
        migrations.AlterUniqueTogether(
            name='remotesystemitem',
            unique_together={('system', 'key')},
        ),
    ]