# Generated by Django 3.1.5 on 2021-06-30 17:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0054_auto_20210630_1740'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='source',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='document_set', to='application.source'),
        ),
    ]