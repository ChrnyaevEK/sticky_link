# Generated by Django 3.1.5 on 2021-04-10 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0016_port_visited'),
    ]

    operations = [
        migrations.AlterField(
            model_name='port',
            name='title',
            field=models.CharField(blank=True, default='Untitled', max_length=200),
        ),
    ]
