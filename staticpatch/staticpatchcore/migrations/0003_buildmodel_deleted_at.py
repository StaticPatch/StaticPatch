# Generated by Django 5.2 on 2025-06-01 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staticpatchcore', '0002_alter_sitemodel_main_domain_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='buildmodel',
            name='deleted_at',
            field=models.DateTimeField(null=True),
        ),
    ]
