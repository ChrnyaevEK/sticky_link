# Generated by Django 3.1.5 on 2021-04-10 13:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0010_port'),
    ]

    operations = [
        migrations.AlterField(
            model_name='port',
            name='wall',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='application.wall'),
        ),
    ]