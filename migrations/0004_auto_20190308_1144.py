# Generated by Django 2.1.3 on 2019-03-08 10:44

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stemp_abw', '0003_auto_20190302_1848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scenario',
            name='data',
            field=django.contrib.postgres.fields.jsonb.JSONField(),
        ),
    ]
