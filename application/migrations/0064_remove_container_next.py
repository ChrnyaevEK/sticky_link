# Generated by Django 3.1.5 on 2021-07-12 15:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0063_auto_20210708_1448'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='container',
            name='next',
        ),
    ]
