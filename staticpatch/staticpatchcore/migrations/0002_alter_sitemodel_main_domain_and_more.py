# Generated by Django 5.1.7 on 2025-04-05 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staticpatchcore', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitemodel',
            name='main_domain',
            field=models.CharField(max_length=500, unique=True),
        ),
        migrations.AlterField(
            model_name='sitemodel',
            name='main_domain_ssl',
            field=models.BooleanField(default=True),
        ),
    ]
