# Generated by Django 3.1.5 on 2021-03-27 19:10

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='container',
            name='description',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Container description'),
        ),
        migrations.AddField(
            model_name='container',
            name='h',
            field=models.IntegerField(default=100, validators=[django.core.validators.MinValueValidator(50)], verbose_name='Container height'),
        ),
        migrations.AddField(
            model_name='container',
            name='index',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Index of container in wall'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='container',
            name='title',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Container title'),
        ),
        migrations.AlterField(
            model_name='wall',
            name='lock_widgets',
            field=models.BooleanField(default=False, verbose_name='Lock widgets at wall'),
        ),
    ]