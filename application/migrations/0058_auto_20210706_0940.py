# Generated by Django 3.1.5 on 2021-07-06 09:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0057_auto_20210701_1501'),
    ]

    operations = [
        migrations.AddField(
            model_name='container',
            name='sync_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='application.container'),
        ),
        migrations.AddField(
            model_name='port',
            name='sync_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='application.port'),
        ),
        migrations.AddField(
            model_name='source',
            name='sync_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='application.source'),
        ),
        migrations.AddField(
            model_name='wall',
            name='sync_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='application.wall'),
        ),
        migrations.AlterField(
            model_name='counter',
            name='container',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.container'),
        ),
        migrations.AlterField(
            model_name='document',
            name='container',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.container'),
        ),
        migrations.AlterField(
            model_name='simplelist',
            name='container',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.container'),
        ),
        migrations.AlterField(
            model_name='simpleswitch',
            name='container',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.container'),
        ),
        migrations.AlterField(
            model_name='simpletext',
            name='container',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.container'),
        ),
        migrations.AlterField(
            model_name='url',
            name='container',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.container'),
        ),
    ]
