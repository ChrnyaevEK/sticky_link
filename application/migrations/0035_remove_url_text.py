# Generated by Django 3.1.5 on 2021-06-06 13:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0034_auto_20210604_1936'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='url',
            name='text',
        ),
    ]
