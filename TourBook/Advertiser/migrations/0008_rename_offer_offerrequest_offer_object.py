# Generated by Django 5.0.2 on 2024-04-19 18:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Advertiser', '0007_rename_offer_object_offerrequest_offer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='offerrequest',
            old_name='offer',
            new_name='offer_object',
        ),
    ]