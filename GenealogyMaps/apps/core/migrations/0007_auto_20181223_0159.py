# Generated by Django 2.1.4 on 2018-12-23 01:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_parish_gen_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parish',
            name='gen_id',
            field=models.IntegerField(default=0, unique=True),
        ),
    ]