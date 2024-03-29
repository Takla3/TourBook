# Generated by Django 5.0.2 on 2024-03-27 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Advertiser', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertiser',
            name='link',
            field=models.URLField(null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='advertiser',
            name='name',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
