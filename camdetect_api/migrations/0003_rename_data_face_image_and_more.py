# Generated by Django 4.2.1 on 2023-05-18 17:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('camdetect_api', '0002_face_user_licenseplate_user_thing_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='face',
            old_name='data',
            new_name='image',
        ),
        migrations.RenameField(
            model_name='licenseplate',
            old_name='data',
            new_name='image',
        ),
        migrations.RenameField(
            model_name='thing',
            old_name='data',
            new_name='image',
        ),
    ]
