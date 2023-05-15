# Generated by Django 4.2.1 on 2023-05-12 18:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('storageapp', '0003_file_created_at_file_user_file_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file_extension',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='storageapp.fileextensions'),
        ),
        migrations.AlterField(
            model_name='file',
            name='file_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='storageapp.filetypes'),
        ),
        migrations.AlterField(
            model_name='file',
            name='user_file_name',
            field=models.CharField(max_length=255),
        ),
    ]
