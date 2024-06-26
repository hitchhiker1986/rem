# Generated by Django 5.0.1 on 2024-03-10 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rem', '0014_alter_apartment_dues_alter_apartment_utilities'),
    ]

    operations = [
        migrations.AddField(
            model_name='apartment',
            name='check_history',
            field=models.ManyToManyField(blank=True, null=True, related_name='apartment_check_history', to='rem.checkhistory'),
        ),
        migrations.AlterField(
            model_name='checkhistory',
            name='description',
            field=models.TextField(default=False, max_length=500),
        ),
    ]
