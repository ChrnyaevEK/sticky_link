# Generated by Django 3.1.5 on 2021-02-20 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0017_wall_h'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wall',
            name='w',
            field=models.IntegerField(default=900, verbose_name='Wall width'),
        ),
    ]
