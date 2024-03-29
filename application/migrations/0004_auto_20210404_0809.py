# Generated by Django 3.1.5 on 2021-04-04 08:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0003_container_w'),
    ]

    operations = [
        migrations.AlterField(
            model_name='counter',
            name='h',
            field=models.IntegerField(default=130, validators=[django.core.validators.MinValueValidator(50)], verbose_name='Widget height'),
        ),
        migrations.AlterField(
            model_name='simplelist',
            name='h',
            field=models.IntegerField(default=130, validators=[django.core.validators.MinValueValidator(50)], verbose_name='Widget height'),
        ),
        migrations.AlterField(
            model_name='simpleswitch',
            name='h',
            field=models.IntegerField(default=130, validators=[django.core.validators.MinValueValidator(50)], verbose_name='Widget height'),
        ),
        migrations.AlterField(
            model_name='simpletext',
            name='h',
            field=models.IntegerField(default=130, validators=[django.core.validators.MinValueValidator(50)], verbose_name='Widget height'),
        ),
        migrations.AlterField(
            model_name='url',
            name='h',
            field=models.IntegerField(default=130, validators=[django.core.validators.MinValueValidator(50)], verbose_name='Widget height'),
        ),
    ]
