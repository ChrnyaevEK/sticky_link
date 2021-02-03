# Generated by Django 3.1.5 on 2021-02-01 22:47

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0005_auto_20210201_2236'),
    ]

    operations = [
        migrations.AddField(
            model_name='richtext',
            name='z_index',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Widget z index(stack position)'),
        ),
        migrations.AddField(
            model_name='simplelist',
            name='z_index',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Widget z index(stack position)'),
        ),
        migrations.AddField(
            model_name='simpletext',
            name='z_index',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Widget z index(stack position)'),
        ),
        migrations.AddField(
            model_name='url',
            name='z_index',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Widget z index(stack position)'),
        ),
    ]