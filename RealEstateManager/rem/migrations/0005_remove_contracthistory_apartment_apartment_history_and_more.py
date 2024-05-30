# Generated by Django 5.0.1 on 2024-02-13 16:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rem', '0004_alter_todo_end_day_alter_todo_start_day'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contracthistory',
            name='apartment',
        ),
        migrations.AddField(
            model_name='apartment',
            name='history',
            field=models.ManyToManyField(related_name='apartment_history', to='rem.contracthistory'),
        ),
        migrations.AlterField(
            model_name='todo',
            name='end_day',
            field=models.DateField(default=datetime.datetime(2024, 2, 13, 16, 44, 13, 898307)),
        ),
        migrations.AlterField(
            model_name='todo',
            name='start_day',
            field=models.DateField(default=datetime.datetime(2024, 2, 13, 16, 44, 13, 898291)),
        ),
    ]
