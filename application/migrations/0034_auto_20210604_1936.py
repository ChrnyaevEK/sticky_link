# Generated by Django 3.1.5 on 2021-06-04 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0033_container_grid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='container',
            name='w',
            field=models.IntegerField(default=3000, verbose_name='Container width'),
        ),
    ]
