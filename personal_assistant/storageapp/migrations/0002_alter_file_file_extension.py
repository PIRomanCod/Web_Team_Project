# Generated by Django 4.2.1 on 2023-05-12 17:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('storageapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file_extension',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='storageapp.fileextensions'),
        ),
    ]
