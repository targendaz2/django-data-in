# Generated by Django 4.1.5 on 2023-01-22 19:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_in', '0003_transformmap'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transformmap',
            old_name='content_type',
            new_name='target',
        ),
        migrations.RemoveField(
            model_name='transformmap',
            name='object_id',
        ),
    ]
