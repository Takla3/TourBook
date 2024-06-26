# Generated by Django 5.0.2 on 2024-05-12 22:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Client', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='comments_field',
        ),
        migrations.AddField(
            model_name='comment',
            name='comment',
            field=models.TextField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='comment',
            name='client_object',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='client_comments', to='Client.client'),
        ),
    ]
