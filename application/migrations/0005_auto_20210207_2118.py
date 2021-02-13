# Generated by Django 3.1.5 on 2021-02-07 21:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('application', '0004_auto_20210207_2102'),
    ]

    operations = [
        migrations.RenameField(
            model_name='wall',
            old_name='view_anonymous',
            new_name='allowed_anonymous',
        ),
        migrations.RemoveField(
            model_name='wall',
            name='change_anonymous',
        ),
        migrations.RemoveField(
            model_name='wall',
            name='change_users',
        ),
        migrations.RemoveField(
            model_name='wall',
            name='view_users',
        ),
        migrations.AddField(
            model_name='wall',
            name='allowed_users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='List of allowed users'),
        ),
        migrations.AlterField(
            model_name='wall',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wall_owner', to=settings.AUTH_USER_MODEL),
        ),
    ]