# Generated by Django 2.2.2 on 2020-03-22 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_auto_20200322_1026'),
    ]

    operations = [
        migrations.AddField(
            model_name='parish',
            name='visible',
            field=models.BooleanField(db_index=True, default=True, help_text='Czy parafia ma być widoczna na mapie/liście'),
        ),
    ]