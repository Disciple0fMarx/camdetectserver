# Generated by Django 4.2.1 on 2023-05-23 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('camdetect_api', '0005_licenseplateprediction_faceprediction'),
    ]

    operations = [
        migrations.AddField(
            model_name='faceprediction',
            name='result',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='licenseplateprediction',
            name='result',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]