# Generated by Django 5.0.1 on 2024-03-25 20:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rem', '0018_remove_apartment_check_history_remove_apartment_dues_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='contracthistory',
            name='apt',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Apartment', to='rem.apartment'),
        ),
    ]