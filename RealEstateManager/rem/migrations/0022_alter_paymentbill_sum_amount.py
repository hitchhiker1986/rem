# Generated by Django 5.0.1 on 2024-03-30 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rem', '0021_alter_paymentbill_amount_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentbill',
            name='sum_amount',
            field=models.FloatField(blank=True, null=True),
        ),
    ]