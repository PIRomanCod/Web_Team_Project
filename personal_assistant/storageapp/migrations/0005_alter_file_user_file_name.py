# Generated by Django 4.2.1 on 2023-05-12 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storageapp', '0004_alter_file_file_extension_alter_file_file_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='user_file_name',
            field=models.CharField(default='old_files', max_length=255),
        ),
    ]
