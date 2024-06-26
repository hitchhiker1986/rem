# Generated by Django 5.0.1 on 2024-03-06 20:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rem', '0008_checkhistory'),
    ]

    operations = [
        migrations.CreateModel(
            name='Deposit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('due_date', models.DateField()),
                ('payment_date', models.DateField(auto_now_add=True)),
                ('payment_amount', models.FloatField(default=0)),
                ('payment_currency', models.CharField(max_length=3)),
                ('payment_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rem.owner')),
            ],
        ),
        migrations.DeleteModel(
            name='PaymentHistory',
        ),
    ]
