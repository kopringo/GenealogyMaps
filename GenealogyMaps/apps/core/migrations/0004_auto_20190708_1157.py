# Generated by Django 2.2.2 on 2019-07-08 11:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20190708_1003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parish',
            name='diocese',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.Diocese'),
        ),
    ]
