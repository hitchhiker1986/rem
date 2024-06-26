# Generated by Django 5.0.1 on 2024-03-07 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rem', '0010_remove_owner_user_owner_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apartment',
            name='contract_start',
        ),
        migrations.AddField(
            model_name='apartment',
            name='balcony_size',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='apartment',
            name='district',
            field=models.CharField(default='', max_length=6),
        ),
        migrations.AddField(
            model_name='apartment',
            name='floor',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name='apartment',
            name='furnished',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='apartment',
            name='halfrooms',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='apartment',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='apartment',
            name='rooms',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='apartment',
            name='size',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='apartment',
            name='topographical_nr',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='apartment',
            name='zip',
            field=models.IntegerField(default=0),
        ),
    ]
