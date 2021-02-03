# Generated by Django 3.1.5 on 2021-02-02 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0006_auto_20210201_2247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='richtext',
            name='background_color',
            field=models.CharField(choices=[('primary', 'Primary'), ('secondary', 'Secondary'), ('success', 'Success'), ('danger', 'Danger'), ('warning', 'Warning'), ('info', 'Info'), ('white', 'White'), ('black', 'Black')], default='white', max_length=10),
        ),
        migrations.AlterField(
            model_name='simplelist',
            name='background_color',
            field=models.CharField(choices=[('primary', 'Primary'), ('secondary', 'Secondary'), ('success', 'Success'), ('danger', 'Danger'), ('warning', 'Warning'), ('info', 'Info'), ('white', 'White'), ('black', 'Black')], default='white', max_length=10),
        ),
        migrations.AlterField(
            model_name='simplelist',
            name='text_color',
            field=models.CharField(choices=[('primary', 'Primary'), ('secondary', 'Secondary'), ('success', 'Success'), ('danger', 'Danger'), ('warning', 'Warning'), ('info', 'Info'), ('white', 'White'), ('black', 'Black')], default='black', max_length=10),
        ),
        migrations.AlterField(
            model_name='simpletext',
            name='background_color',
            field=models.CharField(choices=[('primary', 'Primary'), ('secondary', 'Secondary'), ('success', 'Success'), ('danger', 'Danger'), ('warning', 'Warning'), ('info', 'Info'), ('white', 'White'), ('black', 'Black')], default='white', max_length=10),
        ),
        migrations.AlterField(
            model_name='simpletext',
            name='text_color',
            field=models.CharField(choices=[('primary', 'Primary'), ('secondary', 'Secondary'), ('success', 'Success'), ('danger', 'Danger'), ('warning', 'Warning'), ('info', 'Info'), ('white', 'White'), ('black', 'Black')], default='black', max_length=10),
        ),
        migrations.AlterField(
            model_name='url',
            name='background_color',
            field=models.CharField(choices=[('primary', 'Primary'), ('secondary', 'Secondary'), ('success', 'Success'), ('danger', 'Danger'), ('warning', 'Warning'), ('info', 'Info'), ('white', 'White'), ('black', 'Black')], default='white', max_length=10),
        ),
        migrations.AlterField(
            model_name='url',
            name='text_color',
            field=models.CharField(choices=[('primary', 'Primary'), ('secondary', 'Secondary'), ('success', 'Success'), ('danger', 'Danger'), ('warning', 'Warning'), ('info', 'Info'), ('white', 'White'), ('black', 'Black')], default='black', max_length=10),
        ),
    ]