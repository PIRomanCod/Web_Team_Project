# Generated by Django 4.2.1 on 2023-05-16 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contactapp', '0005_alter_contact_birth_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='birth_date',
            field=models.DateField(blank=True, default=None, null=True),
        ),
    ]
