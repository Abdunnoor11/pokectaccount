# Generated by Django 3.2.8 on 2021-10-15 12:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_invest_lender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invest',
            name='lender',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.lender'),
        ),
    ]
