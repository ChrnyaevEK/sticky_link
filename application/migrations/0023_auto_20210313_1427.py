# Generated by Django 3.1.5 on 2021-03-13 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0022_delete_richtext'),
    ]

    operations = [
        migrations.AddField(
            model_name='counter',
            name='_uid',
            field=models.CharField(db_column='uid', max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='simplelist',
            name='_uid',
            field=models.CharField(db_column='uid', max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='simpletext',
            name='_uid',
            field=models.CharField(db_column='uid', max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='url',
            name='_uid',
            field=models.CharField(db_column='uid', max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='wall',
            name='_uid',
            field=models.CharField(db_column='uid', max_length=32, null=True),
        ),
    ]
