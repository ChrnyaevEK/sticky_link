# Generated by Django 3.1.5 on 2021-04-10 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0015_url_open_in_new_window'),
    ]

    operations = [
        migrations.AddField(
            model_name='port',
            name='visited',
            field=models.IntegerField(default=0, help_text='Visit counter'),
        ),
    ]
