# Generated by Django 4.1.5 on 2023-01-22 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_in', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataimport',
            name='success',
            field=models.BooleanField(default=False),
        ),
    ]
