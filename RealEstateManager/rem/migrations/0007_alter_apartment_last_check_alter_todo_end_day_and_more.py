# Generated by Django 5.0.1 on 2024-02-14 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rem', '0006_alter_apartment_last_check_alter_todo_end_day_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apartment',
            name='last_check',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='todo',
            name='end_day',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='todo',
            name='start_day',
            field=models.DateField(),
        ),
    ]
