# Generated by Django 5.0.1 on 2024-03-25 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rem', '0020_checkhistory_apt_todo_responsible_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentbill',
            name='amount_text',
            field=models.CharField(default='', max_length=50),
        ),
    ]
