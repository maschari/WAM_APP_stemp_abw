# Generated by Django 2.1.3 on 2019-06-05 14:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stemp_abw', '0027_regmundemelenergypercapitaresult'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegMunDemThEnergyResult',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
            },
            bases=('stemp_abw.regmun',),
        ),
    ]
