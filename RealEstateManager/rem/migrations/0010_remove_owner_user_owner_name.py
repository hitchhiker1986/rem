# Generated by Django 5.0.1 on 2024-03-06 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rem', '0009_deposit_payment_delete_paymenthistory'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='owner',
            name='user',
        ),
        migrations.AddField(
            model_name='owner',
            name='name',
            field=models.CharField(default='', max_length=50),
        ),
    ]
