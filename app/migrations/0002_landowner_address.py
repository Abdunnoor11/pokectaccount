# Generated by Django 3.1.6 on 2021-11-23 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='landowner',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
    ]
