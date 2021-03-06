# Generated by Django 2.2.2 on 2019-07-08 12:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0004_auto_20190708_1157'),
    ]

    operations = [
        migrations.AddField(
            model_name='courtbook',
            name='owner',
            field=models.ForeignKey(help_text='Osoba dodająca księgę', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='courtbook',
            name='owner_date_created',
            field=models.DateTimeField(blank=True, help_text='Data dodania księgi', null=True),
        ),
        migrations.AddField(
            model_name='courtbook',
            name='owner_note',
            field=models.TextField(blank=True, help_text='Notatka'),
        ),
    ]
