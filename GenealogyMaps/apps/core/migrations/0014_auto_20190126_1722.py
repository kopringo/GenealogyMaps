# Generated by Django 2.1.4 on 2019-01-26 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20190115_2241'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='country',
            options={'verbose_name_plural': 'kraje'},
        ),
        migrations.AlterModelOptions(
            name='diocese',
            options={'verbose_name_plural': 'diecezje'},
        ),
        migrations.AlterModelOptions(
            name='province',
            options={'verbose_name_plural': 'województwa'},
        ),
        migrations.AddField(
            model_name='diocese',
            name='public',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='province',
            name='public',
            field=models.BooleanField(default=False),
        ),
    ]
