# Generated by Django 5.0.1 on 2024-01-21 11:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0004_water_supply'),
    ]

    operations = [
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('measurement_type', models.CharField(max_length=255)),
                ('value', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='WaterSupply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('date', models.DateField()),
            ],
        ),
        migrations.DeleteModel(
            name='Water_supply',
        ),
        migrations.AddField(
            model_name='measurement',
            name='water_supply',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blogapp.watersupply'),
        ),
        migrations.AlterUniqueTogether(
            name='measurement',
            unique_together={('water_supply', 'measurement_type')},
        ),
    ]
