# Generated by Django 5.0.2 on 2024-04-13 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Advertiser', '0002_alter_advertiser_link_alter_advertiser_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='advertiser',
            name='name',
        ),
        migrations.AlterField(
            model_name='offer',
            name='description',
            field=models.TextField(blank=True, max_length=250, null=True),
        ),
    ]