# Generated by Django 4.2.1 on 2023-05-23 16:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('camdetect_api', '0004_alter_face_image_alter_licenseplate_image_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='LicensePlatePrediction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inference_image', models.ImageField(blank=True, null=True, upload_to='uploads/predictions')),
                ('license_plate', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='camdetect_api.licenseplate')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FacePrediction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inference_image', models.ImageField(blank=True, null=True, upload_to='uploads/predictions')),
                ('face', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='camdetect_api.face')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
