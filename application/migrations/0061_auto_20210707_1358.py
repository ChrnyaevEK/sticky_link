# Generated by Django 3.1.5 on 2021-07-07 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0060_video_youtube'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='source',
            field=models.URLField(blank=True, max_length=2048, null=True),
        ),
        migrations.AlterField(
            model_name='port',
            name='redirect_url',
            field=models.URLField(blank=True, default=None, max_length=2048, null=True),
        ),
        migrations.AlterField(
            model_name='url',
            name='href',
            field=models.URLField(blank=True, max_length=2048, null=True),
        ),
        migrations.AlterField(
            model_name='video',
            name='source',
            field=models.URLField(blank=True, max_length=2048, null=True),
        ),
    ]
