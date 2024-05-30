# Generated by Django 5.0.1 on 2024-02-13 14:03

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rem', '0002_dicthistory_apartment_contract_start_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Due',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(max_length=500)),
                ('amount', models.FloatField()),
            ],
        ),
        migrations.AddField(
            model_name='apartment',
            name='check_status',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='apartment',
            name='last_check',
            field=models.DateField(default=datetime.date(2024, 2, 13)),
        ),
        migrations.AddField(
            model_name='apartment',
            name='next_check',
            field=models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)]),
        ),
        migrations.AddField(
            model_name='apartment',
            name='dues',
            field=models.ManyToManyField(related_name='apartment_dues', to='rem.due'),
        ),
    ]