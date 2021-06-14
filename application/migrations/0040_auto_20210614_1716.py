# Generated by Django 3.1.5 on 2021-06-14 17:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0039_remove_source_wall'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='source',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='application.source'),
        ),
        migrations.AlterField(
            model_name='source',
            name='file',
            field=models.FileField(null=True, upload_to='uploads/%Y/%m/%d/'),
        ),
    ]
