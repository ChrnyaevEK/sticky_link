# Generated by Django 3.1.5 on 2021-04-10 13:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0008_auto_20210410_1255'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='container',
            name='uid',
        ),
        migrations.RemoveField(
            model_name='counter',
            name='uid',
        ),
        migrations.RemoveField(
            model_name='simplelist',
            name='uid',
        ),
        migrations.RemoveField(
            model_name='simpleswitch',
            name='uid',
        ),
        migrations.RemoveField(
            model_name='simpletext',
            name='uid',
        ),
        migrations.RemoveField(
            model_name='url',
            name='uid',
        ),
        migrations.RemoveField(
            model_name='wall',
            name='uid',
        ),
    ]
