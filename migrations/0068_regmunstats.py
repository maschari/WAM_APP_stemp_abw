# Generated by Django 2.1.3 on 2019-02-21 19:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stemp_abw', '0067_auto_20190216_1309'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegMunStats',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
            },
            bases=('stemp_abw.regmun',),
        ),
    ]
