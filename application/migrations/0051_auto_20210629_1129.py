# Generated by Django 3.1.5 on 2021-06-29 11:29

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('application', '0050_auto_20210628_1930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wall',
            name='trusted_users',
            field=models.ManyToManyField(blank=True, related_name='trusted_walls', to=settings.AUTH_USER_MODEL),
        ),
    ]
