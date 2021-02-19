# Generated by Django 3.1.5 on 2021-02-19 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0013_auto_20210213_1550'),
    ]

    operations = [
        migrations.RenameField(
            model_name='counter',
            old_name='height',
            new_name='h',
        ),
        migrations.RenameField(
            model_name='counter',
            old_name='width',
            new_name='w',
        ),
        migrations.RenameField(
            model_name='counter',
            old_name='left',
            new_name='x',
        ),
        migrations.RenameField(
            model_name='counter',
            old_name='top',
            new_name='y',
        ),
        migrations.RenameField(
            model_name='counter',
            old_name='z_index',
            new_name='z',
        ),
        migrations.RenameField(
            model_name='richtext',
            old_name='height',
            new_name='h',
        ),
        migrations.RenameField(
            model_name='richtext',
            old_name='width',
            new_name='w',
        ),
        migrations.RenameField(
            model_name='richtext',
            old_name='left',
            new_name='x',
        ),
        migrations.RenameField(
            model_name='richtext',
            old_name='top',
            new_name='y',
        ),
        migrations.RenameField(
            model_name='richtext',
            old_name='z_index',
            new_name='z',
        ),
        migrations.RenameField(
            model_name='simplelist',
            old_name='height',
            new_name='h',
        ),
        migrations.RenameField(
            model_name='simplelist',
            old_name='width',
            new_name='w',
        ),
        migrations.RenameField(
            model_name='simplelist',
            old_name='left',
            new_name='x',
        ),
        migrations.RenameField(
            model_name='simplelist',
            old_name='top',
            new_name='y',
        ),
        migrations.RenameField(
            model_name='simplelist',
            old_name='z_index',
            new_name='z',
        ),
        migrations.RenameField(
            model_name='simpletext',
            old_name='height',
            new_name='h',
        ),
        migrations.RenameField(
            model_name='simpletext',
            old_name='width',
            new_name='w',
        ),
        migrations.RenameField(
            model_name='simpletext',
            old_name='left',
            new_name='x',
        ),
        migrations.RenameField(
            model_name='simpletext',
            old_name='top',
            new_name='y',
        ),
        migrations.RenameField(
            model_name='simpletext',
            old_name='z_index',
            new_name='z',
        ),
        migrations.RenameField(
            model_name='url',
            old_name='height',
            new_name='h',
        ),
        migrations.RenameField(
            model_name='url',
            old_name='width',
            new_name='w',
        ),
        migrations.RenameField(
            model_name='url',
            old_name='left',
            new_name='x',
        ),
        migrations.RenameField(
            model_name='url',
            old_name='top',
            new_name='y',
        ),
        migrations.RenameField(
            model_name='url',
            old_name='z_index',
            new_name='z',
        ),
        migrations.AlterField(
            model_name='url',
            name='text',
            field=models.CharField(blank=True, max_length=2048, null=True),
        ),
    ]
