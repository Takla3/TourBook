# Generated by Django 5.0.2 on 2024-05-12 14:48

import Core.helpers
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Advertiser', '0001_initial'),
        ('Core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tour',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, max_length=1000, null=True)),
                ('starting_place', models.CharField(max_length=100)),
                ('like_counter', models.IntegerField(default=0)),
                ('dislike_counter', models.IntegerField(default=0)),
                ('seat_num', models.IntegerField(default=0)),
                ('seat_cost', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('transportation_cost', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('extra_cost', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('total_cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('x_starting_place', models.IntegerField(default=0)),
                ('y_starting_place', models.IntegerField(default=0)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('note', models.TextField(blank=True, null=True)),
                ('posted', models.BooleanField(default=0)),
                ('posted_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TourAttachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('attachment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='Core.attachment')),
                ('tour_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tour_attachments', to='Tour_Organizer.tour')),
            ],
            options={
                'db_table': 'tour_attachments',
            },
        ),
        migrations.CreateModel(
            name='TourOrganizer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('address', models.CharField(max_length=255, null=True)),
                ('evaluation', models.IntegerField(default=0)),
                ('logo', models.ImageField(blank=True, null=True, upload_to=Core.helpers.upload_to)),
                ('joined_at', models.DateTimeField(auto_now_add=True)),
                ('situation', models.CharField(choices=[('SUB', 'Subscriper'), ('UNSUB', 'UnSubscriper'), ('B', 'Blocked')], default='UNSUB', max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='organizer', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='tour',
            name='tour_organizer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Tour_Organizer.tourorganizer'),
        ),
        migrations.CreateModel(
            name='TourPoint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('position', models.IntegerField(default=0)),
                ('description', models.TextField(blank=True, max_length=1000, null=True)),
                ('arrival_time', models.DateTimeField()),
                ('leaving_time', models.DateTimeField()),
                ('axis_x', models.IntegerField(default=0)),
                ('axis_y', models.IntegerField(default=0)),
                ('offer_request', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='offer_point_request', to='Advertiser.offerrequest')),
                ('tour_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tour_points', to='Tour_Organizer.tour')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
