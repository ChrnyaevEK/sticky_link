# Generated by Django 3.1.5 on 2021-06-14 16:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0038_document_source'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='source',
            name='wall',
        ),
    ]
