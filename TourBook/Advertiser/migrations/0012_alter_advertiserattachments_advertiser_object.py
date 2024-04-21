# Generated by Django 5.0.2 on 2024-04-19 18:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Advertiser', '0011_rename_attachment_advertiserattachments_attachment_object'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertiserattachments',
            name='advertiser_object',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='advertiser_attachments', to='Advertiser.advertiser'),
        ),
    ]