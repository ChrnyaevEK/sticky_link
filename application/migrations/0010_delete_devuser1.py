# Generated by Django 3.1.5 on 2021-02-13 12:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0003_logentry_add_action_flag_choices'),
        ('application', '0009_auto_20210213_1208'),
    ]

    operations = [
        migrations.DeleteModel(
            name='DevUser1',
        ),
    ]