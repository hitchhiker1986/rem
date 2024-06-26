# Generated by Django 5.0.1 on 2024-04-03 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rem', '0024_alter_apartment_sent_contract'),
    ]

    operations = [
        migrations.AddField(
            model_name='apartment',
            name='child_acceptance_statement',
            field=models.FileField(blank=True, null=True, upload_to='Documents/'),
        ),
        migrations.AddField(
            model_name='apartment',
            name='leave_statement',
            field=models.FileField(blank=True, null=True, upload_to='Documents/'),
        ),
        migrations.AddField(
            model_name='apartment',
            name='signed_contract',
            field=models.FileField(blank=True, null=True, upload_to='Documents'),
        ),
        migrations.AddField(
            model_name='apartment',
            name='takeover_checklist',
            field=models.FileField(blank=True, null=True, upload_to='Documents/'),
        ),
    ]
