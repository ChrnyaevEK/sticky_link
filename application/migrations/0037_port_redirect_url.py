# Generated by Django 3.1.5 on 2021-06-12 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0036_auto_20210606_1528'),
    ]

    operations = [
        migrations.AddField(
            model_name='port',
            name='redirect_url',
            field=models.URLField(default=None, null=True),
        ),
    ]