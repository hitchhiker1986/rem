# Generated by Django 5.0.1 on 2024-03-23 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rem', '0015_apartment_check_history_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bill_number', models.CharField(max_length=20)),
                ('amount', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='PaymentBill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial', models.CharField(max_length=8)),
                ('date', models.DateField(auto_now_add=True)),
                ('issuer', models.CharField(max_length=30)),
                ('issuer_name', models.CharField(max_length=50)),
                ('issuer_address', models.CharField(max_length=50)),
                ('issuer_tax_nr', models.CharField(max_length=20)),
                ('buyer_name', models.CharField(max_length=50)),
                ('buyer_address', models.CharField(max_length=50)),
                ('sum_amount', models.FloatField()),
                ('amount_text', models.TextField()),
                ('cashier', models.CharField(max_length=30)),
            ],
        ),
    ]
