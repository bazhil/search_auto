# Generated by Django 4.0.6 on 2022-08-08 22:03

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import endpoint.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=150)),
                ('description', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Auto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mark', models.CharField(max_length=150)),
                ('model', models.CharField(max_length=150)),
                ('reg_number', models.CharField(max_length=12)),
                ('issue_year', models.PositiveIntegerField(default=2022, validators=[django.core.validators.MinValueValidator(1960), endpoint.models.max_value_current_year])),
                ('vin', models.CharField(max_length=17)),
                ('sts_number', models.CharField(max_length=30)),
                ('sts_date', models.DateField()),
                ('description', models.CharField(blank=True, max_length=300)),
                ('photo', models.ImageField(upload_to='')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='endpoint.categories')),
            ],
        ),
    ]
