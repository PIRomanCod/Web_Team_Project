# Generated by Django 4.2.1 on 2023-05-12 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storageapp', '0011_alter_file_file_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='dropbox_file_name',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
