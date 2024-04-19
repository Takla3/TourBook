# Generated by Django 5.0.2 on 2024-04-19 18:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Advertiser', '0009_rename_quantity_offerrequest_num_of_seat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offerrequest',
            name='offer_object',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='offer_requests', to='Advertiser.offer'),
        ),
    ]
