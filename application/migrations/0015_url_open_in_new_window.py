# Generated by Django 3.1.5 on 2021-04-10 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0014_counter_step'),
    ]

    operations = [
        migrations.AddField(
            model_name='url',
            name='open_in_new_window',
            field=models.BooleanField(default=True),
        ),
    ]
